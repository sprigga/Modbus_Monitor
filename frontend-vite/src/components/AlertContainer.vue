<template>
    <div class="alert-container">
        <div v-for="alert in alerts" :key="alert.id"
             class="alert"
             :class="'alert-' + alert.type">
            <span>{{ alert.message }}</span>
            <button class="btn-close" @click="$emit('remove-alert', alert.id)">&times;</button>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    alerts: Array
});

defineEmits(['remove-alert']);
</script>
