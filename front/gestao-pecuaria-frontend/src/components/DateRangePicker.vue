<template>
  <div>
    <input
      type="text"
      ref="dateInput"
      v-model="displayValue"
      @focus="openCalendar"
      placeholder="Selecione o intervalo"
      class="form-control"
    />
  </div>
</template>

<script>
import flatpickr from 'flatpickr';
import 'flatpickr/dist/flatpickr.css';
import { Portuguese } from 'flatpickr/dist/l10n/pt';

export default {
  data() {
    return {
      startDate: '',
      endDate: '',
      displayValue: '',
      picker: null
    };
  },
  methods: {
    openCalendar() {
      if (this.picker) {
        this.picker.open();
      }
    },
    formatDisplayDate(startDate, endDate) {
      if (startDate && endDate) {
        return `de ${startDate.toLocaleDateString('pt-BR')} até ${endDate.toLocaleDateString('pt-BR')}`;
      }
      return '';
    },
    resetDates() {
      this.startDate = '';
      this.endDate = '';
      this.displayValue = '';
      this.picker.clear(); // Limpa a seleção do flatpickr
      this.$emit('update:startDate', this.startDate);
      this.$emit('update:endDate', this.endDate);
    }
  },
  mounted() {
    this.picker = flatpickr(this.$refs.dateInput, {
      mode: 'range',
      dateFormat: 'd/m/Y',
      locale: Portuguese,
      onChange: (selectedDates) => {
        const [start, end] = selectedDates;
        this.startDate = start ? start.toISOString().split('T')[0] : '';
        this.endDate = end ? end.toISOString().split('T')[0] : '';
        this.displayValue = this.formatDisplayDate(start, end);
        this.$emit('update:startDate', this.startDate);
        this.$emit('update:endDate', this.endDate);
      }
    });
  },
  beforeUnmount() {
    if (this.picker) {
      this.picker.destroy();
    }
  }
};
</script>

<style scoped>
/* Adicione estilos personalizados, se necessário */
</style>
