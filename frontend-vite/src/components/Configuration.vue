<template>
    <div class="glass-card section">
        <h2 class="section-title">
            <i class="fas fa-cog"></i>
            Configuration
        </h2>

        <div class="form-grid">
            <div class="form-group">
                <label>Modbus Host</label>
                <input type="text" class="form-control input-field" :value="config.host" @input="$emit('update:config', { ...config, host: $event.target.value })" placeholder="192.168.1.100">
            </div>
            <div class="form-group">
                <label>Port</label>
                <input type="number" class="form-control input-field" :value="config.port" @input="$emit('update:config', { ...config, port: $event.target.value })" placeholder="502">
            </div>
            <div class="form-group">
                <label>Device ID</label>
                <input type="number" class="form-control input-field" :value="config.device_id" @input="$emit('update:config', { ...config, device_id: $event.target.value })" placeholder="1">
            </div>
            <div class="form-group">
                <label>Poll Interval (seconds)</label>
                <input type="number" step="0.1" class="form-control input-field" :value="config.poll_interval" @input="$emit('update:config', { ...config, poll_interval: $event.target.value })" placeholder="1.0">
            </div>
            <div class="form-group">
                <label>Start Address</label>
                <input type="number" class="form-control input-field" :value="config.start_address" @input="$emit('update:config', { ...config, start_address: $event.target.value })" placeholder="0">
            </div>
            <div class="form-group">
                <label>End Address</label>
                <input type="number" class="form-control input-field" :value="config.end_address" @input="$emit('update:config', { ...config, end_address: $event.target.value })" placeholder="10">
            </div>
        </div>

        <div class="btn-group">
            <button class="btn" @click="handleUpdateConfig" :disabled="loading">
                <i class="fas fa-save"></i> Update Config
            </button>
            <button class="btn" @click="$emit('connect')" :disabled="loading || status.connected">
                <i class="fas fa-plug"></i> Connect
            </button>
            <button class="btn" @click="$emit('disconnect')" :disabled="loading || !status.connected">
                <i class="fas fa-unlink"></i> Disconnect
            </button>
            <button class="btn" @click="$emit('start-monitoring')" :disabled="loading || !status.connected || status.monitoring">
                <i class="fas fa-play"></i> Start Monitoring
            </button>
            <button class="btn" @click="$emit('stop-monitoring')" :disabled="loading || !status.monitoring">
                <i class="fas fa-stop"></i> Stop Monitoring
            </button>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    config: Object,
    status: Object,
    loading: Boolean
});

const emit = defineEmits(['update-config', 'connect', 'disconnect', 'start-monitoring', 'stop-monitoring', 'update:config']);

const handleUpdateConfig = () => {
    emit('update-config');
};
</script>
