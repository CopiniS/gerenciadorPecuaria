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
    cabecalho: {
      type: Array, // Lista de cabeçalhos dinâmicos
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
    mostrarSoma: {
      type: Boolean,
      default: false
    },
    botaoTexto: {
      type: String,
      default: "Gerar Relatório PDF"
    }
  },
  methods: {
    gerarRelatorioPdf() {
      const doc = new jsPDF();
      
      // Adicionar logo
      const logoYPosition = 10;
      doc.addImage(logo, 'PNG', 10, logoYPosition, 30, 30); 

      // Adicionar cabeçalhos dinâmicos no canto superior direito
      doc.setFontSize(12);
      const pageWidth = doc.internal.pageSize.getWidth();
      let yPosition = logoYPosition + 10; // Começar logo após a logo
      const rightMargin = pageWidth - 80; // Ajustar o X para o lado direito

      this.cabecalho.forEach((linha) => {
        doc.text(linha, rightMargin, yPosition, { align: 'right' });
        yPosition += 10;
      });

      // Adicionar título centralizado
      doc.setFontSize(16);
      const titleX = pageWidth / 2;
      doc.text(this.titulo, titleX, yPosition + 20, { align: 'center' });
      
      // Ajustar a posição para começar a tabela
      yPosition += 30;

      // Gerar tabela de dados
      const bodyData = [...this.dados];

      // Soma opcional no final da tabela
      if (this.mostrarSoma) {
        const soma = this.dados.reduce((acc, row) => acc + parseFloat(row[row.length - 1]), 0);
        bodyData.push([...Array(this.colunas.length - 1).fill(''), `Total: ${soma.toFixed(2)}`]);
      }

      doc.autoTable({
        head: [this.colunas],
        body: bodyData,
        startY: yPosition,
        headStyles: { fillColor: [200], textColor: [50] },
        bodyStyles: { fillColor: [245], textColor: [50] },
        alternateRowStyles: { fillColor: [230] },
      });

      // Adicionar data, hora e número da página no rodapé
      const pageCount = doc.internal.getNumberOfPages();
      for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        const date = new Date();
        const emissionDate = date.toLocaleDateString();
        const emissionTime = date.toLocaleTimeString();
        doc.setFontSize(10);
        doc.text(`Emitido em: ${emissionDate} às ${emissionTime}`, 14, doc.internal.pageSize.height - 10);
        doc.text(`Página ${i} de ${pageCount}`, pageWidth - 40, doc.internal.pageSize.height - 10);
      }

      // Salvar o PDF
      const date = new Date();
      const emissionDateForFile = date.toLocaleDateString().replace(/\//g, '-');
      const emissionTimeForFile = date.toLocaleTimeString().replace(/:/g, '-');
      doc.save(`${this.titulo.toLowerCase().replace(/ /g, '_')}_${emissionDateForFile}_${emissionTimeForFile}.pdf`);
    }
  }
}
</script>
