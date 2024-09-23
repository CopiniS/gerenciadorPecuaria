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
    mostrarMedia: {
      type: Boolean,
      default: false
    },
    orientacaoPaisagem: {
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
      // Definir a orientação com base na prop orientacaoPaisagem
      const orientation = this.orientacaoPaisagem ? 'landscape' : 'portrait';
      const doc = new jsPDF(orientation); // Usar a orientação dinâmica
      const pageWidth = doc.internal.pageSize.getWidth();
      const logoYPosition = 10;
      const headerMargin = 80; // Margem esquerda do cabeçalho
      const tableMarginRight = 10; // Margem direita da tabela

      // Adicionar logo
      doc.addImage(logo, 'JPEG', 10, logoYPosition, 30, 30);

      // Adicionar título centralizado
      doc.setFontSize(16);
      const titleX = pageWidth / 2;
      doc.text(this.titulo, titleX, logoYPosition + 40, { align: 'center' });

      // Ajustar a posição para começar a tabela
      let yPosition = logoYPosition + 50;

      // Gerar tabela de dados
      const bodyData = [...this.dados];

      // Soma opcional no final da tabela
      if (this.mostrarSoma) {
        const soma = this.dados.reduce((acc, row) => acc + parseFloat(row[row.length - 1]), 0);
        bodyData.push([...Array(this.colunas.length - 1).fill(''), `Total: ${soma.toFixed(2)}`]);
      }

      // Média opcional no final da tabela
      if (this.mostrarMedia) {
        // Somando os valores
        const total = this.dados.reduce((acc, row) => acc + parseFloat(row[row.length - 1]), 0);

        // Calculando a média (total dividido pelo número de elementos)
        const media = total / this.dados.length;

        // Adicionando a média à tabela
        bodyData.push([...Array(this.colunas.length - 1).fill(''), `Média: ${media.toFixed(2)}`]);
      }


      doc.autoTable({
        head: [this.colunas],
        body: bodyData,
        startY: yPosition,
        headStyles: { fillColor: [200], textColor: [50] },
        bodyStyles: { fillColor: [245], textColor: [50] },
        alternateRowStyles: { fillColor: [230] },
        didDrawPage: (data) => {
          // Adicionar cabeçalhos dinâmicos no canto superior direito
          doc.setFontSize(12);
          const headerX = headerMargin;
          let headerY = logoYPosition + 10; // Começar logo após a logo
          const rightMargin = pageWidth - tableMarginRight; // Margem direita da tabela
          const headerHeight = this.cabecalho.length * 10 + 10; // Altura total do cabeçalho com borda
          const borderRadius = 2; // Raio da borda arredondada
          const borderWidth = 0.3; // Largura da borda

          // Desenhar a borda arredondada ao redor do cabeçalho
          doc.setDrawColor(255, 255, 255); // Cor da borda branca
          doc.setLineWidth(borderWidth);
          doc.roundedRect(headerX - 2, logoYPosition + 5, rightMargin - headerX + 2, headerHeight, borderRadius, borderRadius); // Desenhar o retângulo com bordas arredondadas

          this.cabecalho.forEach((linha) => {
            doc.text(linha, rightMargin, headerY, { align: 'right' });
            headerY += 10;
          });

          // Adicionar data, hora e número da página no rodapé
          const totalPagesExp = "{total_pages_count_string}";
          const pageCount = doc.internal.getNumberOfPages();
          doc.setPage(data.pageNumber);
          const date = new Date();
          const emissionDate = date.toLocaleDateString();
          const emissionTime = date.toLocaleTimeString();
          doc.setFontSize(10);
          doc.text(`Emitido em: ${emissionDate} às ${emissionTime}`, 14, doc.internal.pageSize.height - 10);
          doc.text(`Página ${data.pageNumber} de ${pageCount}`, pageWidth - 40, doc.internal.pageSize.height - 10);

          if (typeof doc.putTotalPages === 'function') {
            doc.putTotalPages(totalPagesExp);
          }
        }
      });

      // Salvar o PDF
      const date = new Date();
      const emissionDateForFile = date.toLocaleDateString().replace(/\//g, '-');
      const emissionTimeForFile = date.toLocaleTimeString().replace(/:/g, '-');
      doc.save(`${this.titulo.toLowerCase().replace(/ /g, '_')}_${emissionDateForFile}_${emissionTimeForFile}.pdf`);
    }
  }
}
</script>
