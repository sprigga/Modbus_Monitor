<template>
    <div id="app">
        <!-- Navigation Bar -->
        <nav class="glass-card navbar">
            <h1 class="navbar-brand">
                <i class="fas fa-network-wired"></i>
                Modbus Monitor
            </h1>
            <div class="navbar-status">
                <span class="status-indicator" :class="statusClass"></span>
                <span>{{ statusText }}</span>
            </div>
        </nav>

        <div class="container">
            <!-- Configuration Section -->
            <Configuration
                :config="config"
                :status="status"
                :loading="loading"
                @update-config="updateConfig"
                @update:config="(val) => Object.assign(config, val)"
                @connect="connect"
                @disconnect="disconnect"
                @start-monitoring="startMonitoring"
                @stop-monitoring="stopMonitoring"
            />

            <!-- Manual Read/Write Section -->
            <div class="two-columns">
                <ManualRead
                    :read-request="readRequest"
                    :status="status"
                    :loading="loading"
                    @read="manualRead"
                    @update:readRequest="(val) => Object.assign(readRequest, val)"
                />
                <WriteRegister
                    :write-request="writeRequest"
                    :multiple-write-values="multipleWriteValues"
                    :status="status"
                    :loading="loading"
                    @write-single="writeSingle"
                    @write-multiple="writeMultiple"
                    @update:writeRequest="(val) => Object.assign(writeRequest, val)"
                    @update:multipleWriteValues="(val) => multipleWriteValues = val"
                />
            </div>

            <!-- Data Display Section -->
            <DataDisplay
                :latest-data="latestData"
                :auto-refresh="autoRefresh"
                @refresh="refreshData"
                @toggle-auto-refresh="toggleAutoRefresh"
            />
        </div>

        <!-- Alerts -->
        <AlertContainer
            :alerts="alerts"
            @remove-alert="removeAlert"
        />
    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue';
import Configuration from './components/Configuration.vue';
import ManualRead from './components/ManualRead.vue';
import WriteRegister from './components/WriteRegister.vue';
import DataDisplay from './components/DataDisplay.vue';
import AlertContainer from './components/AlertContainer.vue';
import api from './services/api.js';
import { useAlerts } from './composables/useAlerts.js';

const { alerts, showAlert, removeAlert } = useAlerts();

// Reactive state
const loading = ref(false);
const autoRefresh = ref(false);
const autoRefreshInterval = ref(null);

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

        isShowingManualRead.value = true;

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
        if (isShowingManualRead.value) {
            await manualRead();
            return;
        }

        const data = await api.get('/data/latest');
        if (data.data) {
            latestData.value = data;
        } else if (data.message) {
            console.log('No data available yet:', data.message);
        }
    } catch (error) {
        console.error('Refresh data error:', error);
        if (error.response && error.response.status !== 404) {
            // Silent fail for no data scenario
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
</script>

<style scoped>
/* All styles are imported from styles.css */
</style>
