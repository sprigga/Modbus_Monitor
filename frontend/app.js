const { createApp, ref, reactive, computed, onMounted, onUnmounted } = Vue;

// API configuration - auto-detect based on environment
const getApiBaseUrl = () => {
    const hostname = window.location.hostname;
    const port = window.location.port;
    
    // If running through nginx proxy (production)
    if (port === '8081' && hostname !== 'localhost') {
        return `${window.location.protocol}//${hostname}:${port}/api`;
    }
    // Development mode
    else if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://localhost:8000/api';
    }
    // Docker or production environment
    else {
        return '/api';
    }
};

const API_BASE_URL = getApiBaseUrl();

createApp({
    setup() {
        // Reactive state
        const loading = ref(false);
        const autoRefresh = ref(false);
        const autoRefreshInterval = ref(null);
        const alerts = ref([]);
        
        const status = reactive({
            connected: false,
            monitoring: false
        });

        const config = reactive({
            host: '192.168.30.20',
            port: 502,
            device_id: 1,
            poll_interval: 2.0,
            timeout: 3.0,
            retries: 3,
            start_address: 1,
            end_address: 26
        });

        const readRequest = reactive({
            address: 1,
            count: 1,
            register_type: 'holding'
        });

        const writeRequest = reactive({
            address: 1,
            value: 0
        });

        const multipleWriteValues = ref('');
        const latestData = ref(null);
        const isShowingManualRead = ref(false);

        // Computed properties
        const statusClass = computed(() => {
            if (status.monitoring) return 'status-monitoring';
            if (status.connected) return 'status-connected';
            return 'status-disconnected';
        });

        const statusText = computed(() => {
            if (status.monitoring) return 'Monitoring';
            if (status.connected) return 'Connected';
            return 'Disconnected';
        });

        // API functions
        const api = {
            async get(endpoint) {
                const response = await axios.get(`${API_BASE_URL}${endpoint}`);
                return response.data;
            },

            async post(endpoint, data = null) {
                const response = await axios.post(`${API_BASE_URL}${endpoint}`, data);
                return response.data;
            }
        };

        // Alert system
        const showAlert = (message, type = 'info') => {
            const id = Date.now();
            alerts.value.push({ id, message, type });
            setTimeout(() => removeAlert(id), 5000);
        };

        const removeAlert = (id) => {
            const index = alerts.value.findIndex(alert => alert.id === id);
            if (index > -1) alerts.value.splice(index, 1);
        };

        // Main functions
        const loadConfig = async () => {
            try {
                const data = await api.get('/config');
                Object.assign(config, data);
            } catch (error) {
                showAlert('Failed to load configuration', 'danger');
                console.error('Load config error:', error);
            }
        };

        const updateConfig = async () => {
            if (loading.value) return;
            
            loading.value = true;
            try {
                await api.post('/config', {
                    host: config.host,
                    port: parseInt(config.port),
                    device_id: parseInt(config.device_id),
                    poll_interval: parseFloat(config.poll_interval),
                    timeout: parseFloat(config.timeout),
                    retries: parseInt(config.retries),
                    start_address: parseInt(config.start_address),
                    end_address: parseInt(config.end_address)
                });
                showAlert('Configuration updated successfully', 'success');
                await checkStatus();
            } catch (error) {
                showAlert('Failed to update configuration', 'danger');
                console.error('Update config error:', error);
            } finally {
                loading.value = false;
            }
        };

        const connect = async () => {
            if (loading.value) return;
            
            loading.value = true;
            try {
                await api.post('/connect');
                showAlert('Connected successfully', 'success');
                await checkStatus();
            } catch (error) {
                showAlert('Failed to connect to Modbus device', 'danger');
                console.error('Connect error:', error);
            } finally {
                loading.value = false;
            }
        };

        const disconnect = async () => {
            if (loading.value) return;
            
            loading.value = true;
            try {
                await api.post('/disconnect');
                showAlert('Disconnected successfully', 'info');
                await checkStatus();
                latestData.value = null;
            } catch (error) {
                showAlert('Failed to disconnect', 'danger');
                console.error('Disconnect error:', error);
            } finally {
                loading.value = false;
            }
        };

        const startMonitoring = async () => {
            if (loading.value) return;
            
            loading.value = true;
            try {
                await api.post('/start_monitoring');
                showAlert('Monitoring started', 'success');
                await checkStatus();
                // Switch back to monitoring mode
                isShowingManualRead.value = false;
                if (!autoRefresh.value) {
                    toggleAutoRefresh();
                }
            } catch (error) {
                showAlert('Failed to start monitoring', 'danger');
                console.error('Start monitoring error:', error);
            } finally {
                loading.value = false;
            }
        };

        const stopMonitoring = async () => {
            if (loading.value) return;
            
            loading.value = true;
            try {
                await api.post('/stop_monitoring');
                showAlert('Monitoring stopped', 'info');
                await checkStatus();
            } catch (error) {
                showAlert('Failed to stop monitoring', 'danger');
                console.error('Stop monitoring error:', error);
            } finally {
                loading.value = false;
            }
        };

        const checkStatus = async () => {
            try {
                const data = await api.get('/status');
                Object.assign(status, data);
            } catch (error) {
                console.error('Status check error:', error);
            }
        };

        const manualRead = async () => {
            if (loading.value) return;
            
            loading.value = true;
            try {
                const data = await api.post('/read', {
                    address: parseInt(readRequest.address),
                    count: parseInt(readRequest.count),
                    register_type: readRequest.register_type
                });
                
                showAlert(`Read successful: ${data.values.join(', ')}`, 'success');
                
                // Set flag to indicate we're showing manual read results
                isShowingManualRead.value = true;
                
                // Display the result in a temporary format
                latestData.value = {
                    data: [{
                        name: `Manual_${readRequest.register_type}_${readRequest.address}`,
                        address: data.address,
                        type: data.type,
                        values: data.values,
                        timestamp: data.timestamp
                    }],
                    timestamp: data.timestamp
                };
            } catch (error) {
                showAlert('Failed to read registers', 'danger');
                console.error('Manual read error:', error);
            } finally {
                loading.value = false;
            }
        };

        const writeSingle = async () => {
            if (loading.value) return;
            
            loading.value = true;
            try {
                await api.post('/write', {
                    address: parseInt(writeRequest.address),
                    value: parseInt(writeRequest.value)
                });
                showAlert(`Successfully wrote value ${writeRequest.value} to address ${writeRequest.address}`, 'success');
            } catch (error) {
                showAlert('Failed to write register', 'danger');
                console.error('Write single error:', error);
            } finally {
                loading.value = false;
            }
        };

        const writeMultiple = async () => {
            if (loading.value || !multipleWriteValues.value.trim()) return;
            
            loading.value = true;
            try {
                const values = multipleWriteValues.value.split(',').map(v => parseInt(v.trim()));
                await api.post('/write_multiple', {
                    address: parseInt(writeRequest.address),
                    values: values
                });
                showAlert(`Successfully wrote ${values.length} values starting at address ${writeRequest.address}`, 'success');
            } catch (error) {
                showAlert('Failed to write multiple registers', 'danger');
                console.error('Write multiple error:', error);
            } finally {
                loading.value = false;
            }
        };

        const refreshData = async () => {
            try {
                // If we're showing manual read results, repeat the manual read
                if (isShowingManualRead.value) {
                    await manualRead();
                    return;
                }
                
                // Otherwise, get monitoring data from Redis
                const data = await api.get('/data/latest');
                // Check if response has data property (actual data)
                if (data.data) {
                    latestData.value = data;
                } else if (data.message) {
                    // Redis has no data yet - this is normal when monitoring just started
                    // Don't show error, just keep current state
                    console.log('No data available yet:', data.message);
                }
            } catch (error) {
                console.error('Refresh data error:', error);
                // Only show error alert if it's not a "no data" situation
                if (error.response && error.response.status !== 404) {
                    // Uncomment below to show error alerts (can be noisy)
                    // showAlert('Failed to refresh data. Check if monitoring is active.', 'warning');
                }
            }
        };

        const toggleAutoRefresh = () => {
            autoRefresh.value = !autoRefresh.value;
            
            if (autoRefresh.value) {
                autoRefreshInterval.value = setInterval(refreshData, 2000);
            } else {
                if (autoRefreshInterval.value) {
                    clearInterval(autoRefreshInterval.value);
                    autoRefreshInterval.value = null;
                }
            }
        };

        const formatTimestamp = (timestamp) => {
            if (!timestamp) return '';
            const date = new Date(timestamp);
            return date.toLocaleString();
        };

        // Lifecycle hooks
        onMounted(async () => {
            await loadConfig();
            await checkStatus();
            
            // Check status periodically
            setInterval(checkStatus, 5000);
        });

        onUnmounted(() => {
            if (autoRefreshInterval.value) {
                clearInterval(autoRefreshInterval.value);
            }
        });

        return {
            // State
            loading,
            autoRefresh,
            alerts,
            status,
            config,
            readRequest,
            writeRequest,
            multipleWriteValues,
            latestData,
            isShowingManualRead,
            
            // Computed
            statusClass,
            statusText,
            
            // Methods
            showAlert,
            removeAlert,
            loadConfig,
            updateConfig,
            connect,
            disconnect,
            startMonitoring,
            stopMonitoring,
            checkStatus,
            manualRead,
            writeSingle,
            writeMultiple,
            refreshData,
            toggleAutoRefresh,
            formatTimestamp
        };
    }
}).mount('#app');