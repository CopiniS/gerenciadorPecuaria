export const masksMixin = {
    methods: {
        valorMask(string) {
            let value = string.replace(/\D/g, '');  // Remove todos os caracteres não numéricos

            // Limita o número de dígitos a 11
            if (value.length > 13) {
                value = value.slice(0, 13);
            }                   
            // Aplica a máscara conforme o comprimento do número
            if (value.length > 12) {
                value = value.replace(/(\d{11})(\d{2})/, '$1,$2');
            //Para o caso de apagar algum valor (Os próximos 5 else if)
            } else if(value.length == 0){
                value = '00,00';
                this.contador = -2;
            } else if(value.length == 1){
                value = value.replace(/(\d)/ , '00,0$1');
                this.contador = 0;
            } else if(value.length == 2){
                value = value.replace(/(\d{2})/ , '00,$1');
                this.contador = 1;
            } else if(value.length == 3){
                value = value.replace(/(\d{1})(\d{2})/ , '0$1,$2');
                this.contador = 2;
            } else if(value.length == 4){
                value = value.replace(/(\d+)(\d{2})/ , '$1,$2');
                this.contador = 3;
            } else if (this.contador > 3){
                value = value.replace(/(\d+)(\d{2})/, '$1,$2');
            } else if (this.contador == 3) {
                value = value.substring(1);
                value = value.replace(/(\d{2})(\d{2})/, '$1,$2');
            } else if (this.contador == 2) {
                value = value.slice(0,1) + value.substring(2);
                value = value.replace(/(0\d)(\d{2})/, '$1,$2');
            } else if (this.contador == 1){
                value = value.slice(0,2) + value.substring(3);
                value = value.replace(/(00)(\d{2})/, '$1,$2');
            } else if(this.contador == 0){
                value = value.replace(/(\d)/, '00,0$1');
            } else if(this.contador == -1){
                //Para o caso de ter sido apagado tudo
                value = value.replace(/0000(\d)/, '00,0$1');
                this.contador += 1;
            } 
            this.contador += 1;
            return value;
        }
    }
  };