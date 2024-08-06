export const masksMixin = {
    methods: {
        valorMask(string){
            // Remove caracteres que não são dígitos ou vírgula
            let value = string.replace(/[^0-9,]/g, '');
            let valueDigitos = string.replace(/\D/g, '');

            // Permite apenas uma vírgula
            const primeiraVirgula = value.indexOf(',');
            if (primeiraVirgula !== -1) {
                value = value.slice(0, primeiraVirgula + 1) + 
                string.slice(primeiraVirgula + 1).replace(/\D/g, '');
            }
            if (valueDigitos.length > 13) {
                value = value.slice(0, 14);
                valueDigitos = valueDigitos.slice(0, 13)
            }
            else if(valueDigitos.length > 3){
                value = value.replace(/^(\d+)(\d{2})$/, '$1,$2');
                
                const regex = /^\d+,\d$/;
                while(regex.test(value)){
                    value = value.replace(/(\d+)(\d),(\d)/, '$1,$2$3');
                    valueDigitos = value.replace(/\D/g, '');
                }

                const regexAposVirgula = /^\d+,\d{2}\d+$/;
                while(regexAposVirgula.test(value)){
                    value = value.replace(/(\d+),(\d)(\d+)/, '$1$2,$3');
                    valueDigitos = value.replace(/\D/g, '');
                }
                const regexPreVirgula = /^0\d\d+,\d{2}/
                while(regexPreVirgula.test(value)){
                    value = value.replace(/0(\d\d+),(\d{2})/, '$1,$2');
                    valueDigitos = value.replace(/\D/g, '');
                }
            }
            else if(valueDigitos.length == 3){
                value = valueDigitos.replace(/^(\d)(\d{2})$/ , '0$1,$2')
                valueDigitos = value.replace(/\D/g, '');
            }
            else if(valueDigitos.length == 2){
                value = valueDigitos.replace(/^(\d{2})$/ , '00,$1')
                valueDigitos = value.replace(/\D/g, '');
            }
            else if(valueDigitos.length == 1){
                value = valueDigitos.replace(/^(\d)$/ , '00,0$1')
                valueDigitos = value.replace(/\D/g, '');
            }
            else{
                value = value.replace(/\D/g, '');
            }

            return value;   
        },

        digitosMask(string){
            let value = string.replace(/\D/g, '');
            if(value.length > 11){
                value = value.slice(0, 11);
            }
            else if(parseInt(value) == 0){
                value = ''
            }
            return value;
        },

        brincoMask(string){
            let value = string.replace(/\D/g, '');
            if(parseInt(value) == 0){
                value = ''
            }
            else if(value.length == 1){
                value = value.replace(/(\d)/, '00000$1')
            }
            else if(value.length == 2){
                value = value.replace(/(\d{2})/, '0000$1')
            }
            else if(value.length == 3){
                value = value.replace(/(\d{3})/, '000$1')
            }
            else if(value.length == 4){
                value = value.replace(/(\d{4})/, '00$1')
            }
            else if(value.length == 5){
                value = value.replace(/(\d{5})/, '0$1')
            }
            else if (value.length > 6) {
                if(value[0] != '0'){
                    value = value.slice(0, 6);
                }
                else{
                    value = value.slice(1)
                }
            }  
            return value;
        },

        brincoFiltroMask(string){
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

        latLongMask(string){
            let valueComSinal = string.replace(/[^0-9+-]/g, '');
            let value = string.replace(/\D/g, '');

            if(value.length == 10 && /^0\d{9}$/.test(value)){
                value = value.replace(/(0)(\d{3})(\d{6})/, '$2,$3')
            } else if(value.length > 9){
                value = value.slice(0, 9);
            }          
            // Aplica a máscara conforme o comprimento do número
            if(value.length == 0){
                value = '';
            } else if(value.length == 1){
                value = value.replace(/(\d)/ , '000,00000$1');
            } else if(value.length == 2){
                value = value.replace(/(\d{2})/ , '000,0000$1');
            } else if(value.length == 3){
                value = value.replace(/(\d{3})/ , '000,000$1');
            } else if(value.length == 4){
                value = value.replace(/(\d{4})/ , '000,00$1');
            } else if(value.length == 5){
                value = value.replace(/(\d{5})/ , '000,0$1');
            } else if(value.length == 6){
                value = value.replace(/(\d{6})/ , '000,$1');
            } else if(value.length == 7){
                value = value.replace(/(\d)(\d{6})/ , '00$1,$2');
            } else if(value.length == 8){
                value = value.replace(/(\d{2})(\d{6})/ , '0$1,$2');
            } else if(value.length == 9){
                value = value.replace(/(\d{3})(\d{6})/ , '$1,$2');
            } 
            


            if(valueComSinal.includes('+') ){
                value = value.replace(/(-)(\d{3},\d{6})/ , '$2')
            }
            else if(valueComSinal.includes('-')){
                value = value.replace(/(\d{3},\d{6})/ , '-$1')
            }
            return value;
        }
    }
  };