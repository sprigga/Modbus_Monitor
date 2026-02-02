<template>
    <div class="glass-card">
        <h3 class="card-title">
            <i class="fas fa-edit"></i>
            Write Holding Register
        </h3>

        <div class="form-group" style="margin-bottom: 16px;">
            <label>Address</label>
            <input type="number" class="form-control input-field" :value="writeRequest.address" @input="$emit('update:writeRequest', { ...writeRequest, address: $event.target.value })" placeholder="0">
        </div>

        <div class="form-group" style="margin-bottom: 16px;">
            <label>Value</label>
            <input type="number" class="form-control input-field" :value="writeRequest.value" @input="$emit('update:writeRequest', { ...writeRequest, value: $event.target.value })" placeholder="100">
        </div>

        <div class="form-group" style="margin-bottom: 20px;">
            <label>Multiple Values (comma-separated)</label>
            <input type="text" class="form-control input-field" :value="multipleWriteValues" @input="$emit('update:multipleWriteValues', $event.target.value)"
                   placeholder="e.g., 100,200,300">
        </div>

        <div class="btn-group">
            <button class="btn" @click="$emit('write-single')" :disabled="loading || !status.connected">
                <i class="fas fa-pen"></i> Write Single
            </button>
            <button class="btn" @click="$emit('write-multiple')" :disabled="loading || !status.connected">
                <i class="fas fa-pen-alt"></i> Write Multiple
            </button>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    writeRequest: Object,
    multipleWriteValues: String,
    status: Object,
    loading: Boolean
});

defineEmits(['write-single', 'write-multiple', 'update:writeRequest', 'update:multipleWriteValues']);
</script>
