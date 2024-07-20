export const masksMixin = {
    methods: {
        valorMask(string) {
            let value = string.replace(/\D/g, '');  // Remove todos os caracteres não numéricos

            // Limita o número de dígitos a 11
            if (value.length > 13) {
                console.log('entra em value.length > 13');
                value = value.slice(0, 13);
            }                   
            console.log('inicial: value: ', value , "  -  contador: ", this.contador);
            // Aplica a máscara conforme o comprimento do número
            if (value.length > 12) {
                console.log('entra em value.length > 12');
                value = value.replace(/(\d{11})(\d{2})/, '$1,$2');
            //Para o caso de apagar algum valor (Os próximos 5 else if)
            } else if(value.length == 0){
                console.log('entra em value.length == 0');
                value = '';
                this.contador = -1;
            } else if(value.length == 1){
                console.log('entra em value.length == 1');
                value = value.replace(/(\d)/ , '00,0$1');
                this.contador = 0;
            } else if(value.length == 2){
                console.log('entra em value.length == 2');
                value = value.replace(/(\d{2})/ , '00,$1');
                this.contador = 1;
            } else if(value.length == 3){
                console.log('entra em value.length == 3');
                value = value.replace(/(\d{1})(\d{2})/ , '0$1,$2');
                this.contador = 2;
            } else if(value.length == 4){
                console.log('entra em value.length == 4');
                value = value.replace(/(\d+)(\d{2})/ , '$1,$2');
                this.contador = 3;
            } else if (this.contador > 3){
                console.log('entra em contador > 3');
                value = value.replace(/(\d+)(\d{2})/, '$1,$2');
            } else if (this.contador == 3) {
                console.log('entra em contador == 3');
                value = value.substring(1);
                value = value.replace(/(\d{2})(\d{2})/, '$1,$2');
            } else if (this.contador == 2) {
                console.log('entra em contador == 2');
                value = value.slice(0,1) + value.substring(2);
                value = value.replace(/(0\d)(\d{2})/, '$1,$2');
            } else if (this.contador == 1){
                console.log('entra em contador == 1');
                value = value.slice(0,2) + value.substring(3);
                value = value.replace(/(00)(\d{2})/, '$1,$2');
            } else if(this.contador == 0){
                console.log('entra em contador == 0');
                value = value.replace(/(\d)/, '00,0$1');
            } 
            this.contador += 1;
            return value;
        },

        brincoMask(string){
            let value = string.replace(/\D/g, '');
            if (value.length > 6) {
                value = value.slice(0, 6);
            }  
            return value;
        },

        observacoesMask(string){
            if (string.length > 255) {
                string = string.slice(0, 255);
            }
            return string; 
        },

        telefoneMask(string) {
            let value = string.replace(/\D/g, '');  // Remove todos os caracteres não numéricos
            
            // Limita o número de dígitos a 11
            if (value.length > 11) {
                value = value.slice(0, 11);
            }
            
            // Aplica a máscara conforme o comprimento do número
            if (value.length > 10) {
                value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
            } else if (value.length > 5) {
                value = value.replace(/(\d{2})(\d{4})(\d+)/, '($1) $2-$3');
            } else if (value.length > 2) {
                value = value.replace(/(\d{2})(\d+)/, '($1) $2');
            } else {
                value = value.replace(/(\d+)/, '($1');
            }
            return value;
        },

        // latLongMask(string){
        //     let valueComSinais = string.replace(/\D | - | +/g, '');
        //     let value = string.replace(/\D/g, '');
            
        //     if(valueComSinais.includes('-')){
        //         return true;
        //     }

        //     // Limita o número de dígitos a 11
        //     if (value.length > 10) {
        //         value = value.slice(0, 10);
        //     } 
        //     console.log('inicial: value: ', value , "  -  contador: ", this.contadorLat);                 
        //     // Aplica a máscara conforme o comprimento do número
        //     if (value.length > 9) {
        //         value = value.replace(/(\d{3})(\d{6})/, '$1,$2');
        //     //Para o caso de apagar algum valor (Os próximos 5 else if)
        //     } else if(value.length == 0){
        //         console.log('entra em value.length == 0');
        //         value = '';
        //         this.contadorLat = -1;
        //     } else if(value.length == 1){
        //         console.log('entra em value.length == 1');
        //         value = value.replace(/(\d)/ , '000,00000$1');
        //         this.contadorLat = 0;
        //     } else if(value.length == 2){
        //         console.log('entra em value.length == 2');
        //         value = value.replace(/(\d{2})/ , '000,0000$1');
        //         this.contadorLat = 1;
        //     } else if(value.length == 3){
        //         console.log('entra em value.length == 3');
        //         value = value.replace(/(\d{3})/ , '000,000$1');
        //         this.contadorLat = 2;
        //     } else if(value.length == 4){
        //         console.log('entra em value.length == 4');
        //         value = value.replace(/(\d{4})/ , '000,00$1');
        //         this.contadorLat = 3;
        //     } else if(value.length == 5){
        //         console.log('entra em value.length == 5');
        //         value = value.replace(/(\d{5})/ , '000,0$1');
        //         this.contadorLat = 4;
        //     } else if(value.length == 6){
        //         console.log('entra em value.length == 6');
        //         value = value.replace(/(\d{6})/ , '000,$1');
        //         this.contadorLat = 5;
        //     } else if(value.length == 7){
        //         console.log('entra em value.length == 7');
        //         value = value.replace(/(\d)(\d{6})/ , '00$1,$2');
        //         this.contadorLat = 6;
        //     } else if(value.length == 8){
        //         console.log('entra em value.length == 8');
        //         value = value.replace(/(\d{2})(\d{6})/ , '0$1,$2');
        //         this.contadorLat = 7;
        //     } else if(value.length == 9){
        //         console.log('entra em value.length == 9');
        //         value = value.replace(/(\d{3})(\d{6})/ , '$1,$2');
        //         this.contador = 8;
        //     } else if (this.contadorLat >= 8){
        //         value = value.substring(1);
        //         console.log('entra em contador > 8');
        //         value = value.replace(/(\d{3})(\d{6})/, '$1,$2');
        //     } else if (this.contadorLat == 7){
        //         value = value.slice(0,1) + value.substring(2);
        //         console.log('entra em contador == 7');
        //         value = value.replace(/(0\d{2})(\d{6})/, '$1,$2');
        //     } else if (this.contadorLat == 6){
        //         value = value.slice(0,2) + value.substring(3);
        //         console.log('entra em contador == 6');
        //         value = value.replace(/(00\d)(\d{6})/, '$1,$2');
        //     } else if (this.contadorLat == 5){
        //         value = value.slice(0,3) + value.substring(4);
        //         console.log('entra em contador == 5');
        //         value = value.replace(/(000)(\d{6})/, '$1,$2');
        //     } else if (this.contadorLat== 4){
        //         console.log('entra em contador == 4');
        //         value = value.slice(0,3) + value.substring(4);
        //         value = value.replace(/(000)(0\d{5})/, '$1,$2');
        //     } else if (this.contadorLat == 3) {
        //         console.log('entra em contador == 3');
        //         value = value.slice(0,3) + value.substring(4);
        //         value = value.replace(/(000)(00\d{4})/, '$1,$2');
        //     } else if (this.contadorLat == 2) {
        //         console.log('entra em contador == 2');
        //         value = value.slice(0,3) + value.substring(4);
        //         value = value.replace(/(000)(000\d{3})/, '$1,$2');
        //     } else if (this.contadorLat == 1){
        //         console.log('entra em contador == 1');
        //         value = value.slice(0,3) + value.substring(4);
        //         value = value.replace(/(000)(0000\d{2})/, '$1,$2');
        //     } else if(this.contadorLat == 0){
        //         console.log('entra em contador == 0');
        //         console.log('entra aqui no 0');
        //         value = value.replace(/(\d)/, '000,00000$1');
        //     } 
        //     this.contadorLat += 1;
        //     return value;
        // }
    }
  };