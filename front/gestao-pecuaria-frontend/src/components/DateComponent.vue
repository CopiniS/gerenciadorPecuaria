<template>
    <div>
      <input
        type="text"
        ref="dateInput"
        v-model="displayValue"
        @focus="openCalendar"
       :placeholder="placeholder"
        class="form-control"
      />
    </div>
  </template>
  
  <script>
  import flatpickr from 'flatpickr';
  import 'flatpickr/dist/flatpickr.css';
  import { Portuguese } from 'flatpickr/dist/l10n/pt';
  
  export default {
    props: {
    placeholder: {
      type: String,
      default: 'Selecione a data',
    },
  },
    data() {
      return {
        selectedDate: '',
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
      formatDisplayDate(date) {
        return date ? date.toLocaleDateString('pt-BR') : '';
      },
      resetDate() {
        this.selectedDate = '';
        this.displayValue = '';
        this.picker.clear(); // Limpa a seleção do flatpickr
        this.$emit('update:selectedDate', this.selectedDate);
      }
    },
    mounted() {
      this.picker = flatpickr(this.$refs.dateInput, {
        mode: 'single', // Muda para modo de data única
        dateFormat: 'd/m/Y',
        locale: Portuguese,
        onChange: (selectedDates) => {
          const [date] = selectedDates;
          this.selectedDate = date ? date.toISOString().split('T')[0] : '';
          this.displayValue = this.formatDisplayDate(date);
          this.$emit('update:selectedDate', this.selectedDate);
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
  