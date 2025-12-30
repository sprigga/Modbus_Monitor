<template>
    <div class="glass-card section">
        <div class="card-header">
            <h3 class="section-title" style="margin: 0;">
                <i class="fas fa-table"></i>
                Modbus Data
            </h3>
            <div>
                <button class="btn btn-small" @click="$emit('refresh')">
                    <i class="fas fa-refresh"></i> Refresh
                </button>
                <button class="btn btn-small" @click="$emit('toggle-auto-refresh')">
                    <i class="fas" :class="autoRefresh ? 'fa-pause' : 'fa-play'"></i>
                    {{ autoRefresh ? 'Pause' : 'Auto' }}
                </button>
            </div>
        </div>

        <div v-if="latestData && latestData.data">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Address</th>
                        <th>Type</th>
                        <th>Values</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="register in latestData.data" :key="register.name">
                        <td>{{ register.name }}</td>
                        <td>{{ register.address }}</td>
                        <td>{{ register.type }}</td>
                        <td>
                            <span class="data-value">
                                {{ register.values.join(', ') }}
                            </span>
                        </td>
                        <td class="timestamp">{{ formatTimestamp(register.timestamp) }}</td>
                    </tr>
                </tbody>
            </table>
            <p class="timestamp" style="margin-top: 16px;">
                Last updated: {{ formatTimestamp(latestData.timestamp) }}
            </p>
        </div>
        <div v-else class="empty-state">
            <i class="fas fa-inbox"></i>
            <p>No data available. Start monitoring to see live data.</p>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    latestData: Object,
    autoRefresh: Boolean
});

defineEmits(['refresh', 'toggle-auto-refresh']);

const formatTimestamp = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleString();
};
</script>
