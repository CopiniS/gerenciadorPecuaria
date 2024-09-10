<template>
    <button @click="gerarRelatorioPdf" class="btn btn-success">{{ botaoTexto }}</button>
  </template>
  
  <script>
  import jsPDF from 'jspdf';
  import 'jspdf-autotable';
  import logo from '/src/assets/logo.jpeg'; 
  
  export default {
    props: {
      titulo: {
        type: String,
        required: true
      },
      produtor: {
        type: String,
        required: true
      },
      colunas: {
        type: Array,
        required: true
      },
      dados: {
        type: Array,
        required: true
      },
      botaoTexto: {
        type: String,
        default: "Gerar Relatório PDF"
      }
    },
    methods: {
      gerarRelatorioPdf() {
        const doc = new jsPDF();
  
        // Adiciona a logo no canto superior esquerdo
        doc.addImage(logo, 'PNG', 10, 10, 30, 30); 
  
        // Adiciona informações de página, data e hora no canto superior direito
        const totalPagesExp = "{total_pages_count_string}";
        // const pageCount = doc.internal.getNumberOfPages();
  
          const date = new Date();
          const emissionDate = date.toLocaleDateString();
          const emissionTime = date.toLocaleTimeString();
          const produtor =  this.produtor;
  
          // Renderiza a informação na primeira página e define o template para as outras páginas
          const footer = function (data) {
          let str = "Página " + data.pageCount;
          if (typeof doc.putTotalPages === 'function') {
            str = str + " de " + totalPagesExp;
          }
  
          doc.setFontSize(10);
          doc.text(str, data.settings.margin.left + 150, 20);
          doc.text(`Emissão: ${emissionDate}`, data.settings.margin.left + 150, 25);
          doc.text(`Hora: ${emissionTime}`, data.settings.margin.left + 150, 30);
          doc.text(`Produtor: ${produtor}`, data.settings.margin.left + 150, 35);
        };
  
        // Adiciona o título do relatório abaixo da logo
        doc.setFontSize(16);
        doc.text(this.titulo, 14, 50);
  
        // Gera a tabela de dados
        doc.autoTable({
          head: [this.colunas],
          body: this.dados,
          startY: 60,
          headStyles: {
            fillColor: [200],
            textColor: [50],
          },
          bodyStyles: {
            fillColor: [245],
            textColor: [50],
          },
          alternateRowStyles: {
            fillColor: [230]
          },
          didDrawPage: footer // Adiciona o rodapé em todas as páginas
        });
  
        // Coloca o total de páginas após gerar o conteúdo
        if (typeof doc.putTotalPages === 'function') {
          doc.putTotalPages(totalPagesExp);
        }
  
        // Salva o arquivo PDF
        doc.save(`${this.titulo.toLowerCase().replace(/ /g, '_')}_${emissionDate.replace(/\//g, '-')}_${emissionTime.replace(/:/g, '-')}.pdf`);
      }
    }
  }
  </script>
  
  <style scoped>
  /* Adicione estilos específicos se necessário */
  </style>
  