import { ref } from 'vue';

const alerts = ref([]);

export function useAlerts() {
    const showAlert = (message, type = 'info') => {
        const id = Date.now();
        alerts.value.push({ id, message, type });
        setTimeout(() => removeAlert(id), 5000);
    };

    const removeAlert = (id) => {
        const index = alerts.value.findIndex(alert => alert.id === id);
        if (index > -1) alerts.value.splice(index, 1);
    };

    return {
        alerts,
        showAlert,
        removeAlert
    };
}
