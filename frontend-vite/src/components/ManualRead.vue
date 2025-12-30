<template>
    <div class="glass-card">
        <h3 class="card-title">
            <i class="fas fa-book-open"></i>
            Manual Read
        </h3>

        <div class="form-group" style="margin-bottom: 16px;">
            <label>Address</label>
            <input type="number" class="form-control input-field" :value="readRequest.address" @input="$emit('update:readRequest', { ...readRequest, address: $event.target.value })" placeholder="0">
        </div>

        <div class="form-group" style="margin-bottom: 16px;">
            <label>Count</label>
            <input type="number" class="form-control input-field" :value="readRequest.count" @input="$emit('update:readRequest', { ...readRequest, count: $event.target.value })" placeholder="1">
        </div>

        <div class="form-group" style="margin-bottom: 20px;">
            <label>Register Type</label>
            <select class="form-control input-field" :value="readRequest.register_type" @input="$emit('update:readRequest', { ...readRequest, register_type: $event.target.value })">
                <option value="holding">Holding Registers</option>
                <option value="input">Input Registers</option>
                <option value="coils">Coils</option>
                <option value="discrete_inputs">Discrete Inputs</option>
            </select>
        </div>

        <button class="btn" @click="$emit('read')" :disabled="loading || !status.connected">
            <i class="fas fa-search"></i> Read
        </button>
    </div>
</template>

<script setup>
const props = defineProps({
    readRequest: Object,
    status: Object,
    loading: Boolean
});

defineEmits(['read', 'update:readRequest']);
</script>
