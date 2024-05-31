-- COMPONENTE COMPRA PRODUTO

-- Função para atualizar o estoque após o insert da compra
CREATE OR REPLACE FUNCTION trigger_inserir_compraproduto() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_produto
    SET estoque = estoque + NEW."quantidadeComprada"
    WHERE id = NEW.produto_id;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Função para atualizar o estoque após o delete da compra
CREATE OR REPLACE FUNCTION trigger_excluir_compraproduto() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_produto
    SET estoque = estoque - OLD."quantidadeComprada"
    WHERE id = OLD.produto_id;
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

--Função para atualizar o estoque após o update da compra
CREATE OR REPLACE FUNCTION trigger_atualizar_compraproduto() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_produto
    SET estoque = estoque - OLD."quantidadeComprada" + NEW."quantidadeComprada"
    WHERE id = NEW.produto_id;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o insert
CREATE TRIGGER apos_inserir_compra
AFTER INSERT ON core_compraproduto
FOR EACH ROW
EXECUTE FUNCTION trigger_inserir_compraproduto();

-- Trigger que dispara após o delete
CREATE TRIGGER apos_excluir_compra
AFTER DELETE ON core_compraproduto
FOR EACH ROW
EXECUTE FUNCTION trigger_excluir_compraproduto();

-- Trigger que dispara após o update
CREATE TRIGGER apos_atualizar_compra
AFTER UPDATE ON core_compraproduto
FOR EACH ROW
EXECUTE FUNCTION trigger_atualizar_compraproduto();



-- COMPONENTE SUPLEMENTAÇÃO

-- Função para atualizar o estoque após o insert da suplementacao
CREATE OR REPLACE FUNCTION trigger_inserir_suplementacao() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_produto
    SET estoque = estoque - NEW.quantidade
    WHERE id = NEW.produto_id;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Função para atualizar o estoque após o delete da suplementação
CREATE OR REPLACE FUNCTION trigger_excluir_suplementacao() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_produto
    SET estoque = estoque + OLD.quantidade
    WHERE id = OLD.produto_id;
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

--Função para atualizar o estoque após o update da compra
CREATE OR REPLACE FUNCTION trigger_atualizar_suplementacao() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_produto
    SET estoque = estoque + OLD.quantidade - NEW.quantidade
    WHERE id = NEW.produto_id;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o insert
CREATE TRIGGER apos_inserir_suplementacao
AFTER INSERT ON core_suplementacao
FOR EACH ROW
EXECUTE FUNCTION trigger_inserir_suplementacao();

-- Trigger que dispara após o delete
CREATE TRIGGER apos_excluir_suplementacao
AFTER DELETE ON core_suplementacao
FOR EACH ROW
EXECUTE FUNCTION trigger_excluir_suplementacao();

-- Trigger que dispara após o update
CREATE TRIGGER apos_atualizar_suplementacao
AFTER UPDATE ON core_suplementacao
FOR EACH ROW
EXECUTE FUNCTION trigger_atualizar_suplementacao();


-- COMPONENTE APLICACAO DE PRODUTOS

-- Função para atualizar o estoque após o insert da aplicacaoProdutos
CREATE OR REPLACE FUNCTION trigger_inserir_aplicacaoproduto() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_produto
    SET estoque = estoque - NEW.dosagem
    WHERE id = NEW.produto_id;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Função para atualizar o estoque após o delete da aplicacaoProdutos
CREATE OR REPLACE FUNCTION trigger_excluir_aplicacaoproduto() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_produto
    SET estoque = estoque + OLD.dosagem
    WHERE id = OLD.produto_id;
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Função para atualizar o estoque após o update da aplicacaoProdutos
CREATE OR REPLACE FUNCTION trigger_atualizar_aplicacaoproduto() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_produto
    SET estoque = estoque + OLD.dosagem - NEW.dosagem
    WHERE id = NEW.produto_id;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER apos_inserir_aplicacao
AFTER INSERT ON core_aplicacaoproduto
FOR EACH ROW
EXECUTE FUNCTION trigger_inserir_aplicacaoproduto();

CREATE TRIGGER apos_excluir_aplicacao
AFTER DELETE ON core_aplicacaoproduto
FOR EACH ROW
EXECUTE FUNCTION trigger_excluir_aplicacaoproduto();

CREATE TRIGGER apos_atualizar_aplicacao
AFTER UPDATE ON core_aplicacaoproduto
FOR EACH ROW
EXECUTE FUNCTION trigger_atualizar_aplicacaoproduto();


-- COMPONENTE VENDA DE ANIMAIS

-- Função para atualizar o status do animal após o insert da venda
CREATE OR REPLACE FUNCTION trigger_inserir_vendaanimal() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_animal
    SET status = 'Vendido', "dataBaixa" = NEW."dataVenda"
    WHERE id = NEW.animal_id;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Função para atualizar o status do animal após o delete da venda
CREATE OR REPLACE FUNCTION trigger_excluir_vendaanimal() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_animal
    SET status = 'Vivo', "dataBaixa" = NULL
    WHERE id = OLD.animal_id;
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Função para atualizar o status do animal após o update da venda
CREATE OR REPLACE FUNCTION trigger_atualizar_vendaanimal() RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se o animal_id foi alterado
    IF OLD.animal_id IS DISTINCT FROM NEW.animal_id THEN
        -- Atualiza status do animal antigo
        UPDATE core_animal
        SET status = 'Vivo', "dataBaixa" = NULL
        WHERE id = OLD.animal_id;
        
        -- Atualiza status do novo animal
        UPDATE core_animal
        SET status = 'Vendido', "dataBaixa" = NEW."dataVenda"
        WHERE id = NEW.animal_id;
    END IF;

    -- Verifica se a data de venda foi alterada
    IF OLD."dataVenda" IS DISTINCT FROM NEW."dataVenda" THEN
        -- Atualiza dataBaixa
        UPDATE core_animal
        SET "dataBaixa" = NEW."dataVenda"
        WHERE id = NEW.animal_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o insert
CREATE TRIGGER apos_inserir_vendaanimal
AFTER INSERT ON core_vendaanimal
FOR EACH ROW
EXECUTE FUNCTION trigger_inserir_vendaanimal();

-- Trigger que dispara após o delete
CREATE TRIGGER apos_excluir_vendaanimal
AFTER DELETE ON core_vendaanimal
FOR EACH ROW
EXECUTE FUNCTION trigger_excluir_vendaanimal();

-- Trigger que dispara após o update
CREATE TRIGGER apos_atualizar_vendaanimal
AFTER UPDATE ON core_vendaanimal
FOR EACH ROW
EXECUTE FUNCTION trigger_atualizar_vendaanimal();


-- COMPONENTE OCORRENCIAS DE ANIMAIS

-- Função para atualizar o status do animal após o insert da ocorrência
CREATE OR REPLACE FUNCTION trigger_inserir_ocorrencia() RETURNS TRIGGER AS $$
BEGIN
	IF NEW.tipo = 'Morte' THEN
		UPDATE core_animal
		SET status = 'Morto', "dataBaixa" = NEW."dataOcorrencia"
		WHERE id = NEW.animal_id;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Função para atualizar o status do animal após o delete da ocorrencia
CREATE OR REPLACE FUNCTION trigger_excluir_ocorrencia() RETURNS TRIGGER AS $$
BEGIN
	IF OLD.tipo = 'Morte' THEN
		UPDATE core_animal
		SET status = 'Vivo', "dataBaixa" = NULL
		WHERE id = OLD.animal_id;
	END IF;
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Função para atualizar o status do animal após o update da ocorrencia
CREATE OR REPLACE FUNCTION trigger_atualizar_ocorrencia() RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se o animal_id foi alterado
    IF OLD.animal_id IS DISTINCT FROM NEW.animal_id THEN
        -- Atualiza status do animal antigo
        UPDATE core_animal
        SET status = 'Vivo', "dataBaixa" = NULL
        WHERE id = OLD.animal_id;
        
        -- Atualiza status do novo animal
        UPDATE core_animal
        SET status = 'Vendido', "dataBaixa" = NEW."dataOcorrencia"
        WHERE id = NEW.animal_id;
    END IF;

    -- Verifica se a data de ocorrencia foi alterada
    IF OLD."dataOcorrencia" IS DISTINCT FROM NEW."dataOcorrencia" THEN
        -- Atualiza dataBaixa
        UPDATE core_animal
        SET "dataBaixa" = NEW."dataOcorrencia"
        WHERE id = NEW.animal_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o insert
CREATE TRIGGER apos_inserir_ocorrencia
AFTER INSERT ON core_ocorrencia
FOR EACH ROW
EXECUTE FUNCTION trigger_inserir_ocorrencia();

-- Trigger que dispara após o delete
CREATE TRIGGER apos_excluir_ocorrencia
AFTER DELETE ON core_ocorrencia
FOR EACH ROW
EXECUTE FUNCTION trigger_excluir_ocorrencia();

-- Trigger que dispara após o update
CREATE TRIGGER apos_atualizar_ocorrencia
AFTER UPDATE ON core_ocorrencia
FOR EACH ROW
EXECUTE FUNCTION trigger_atualizar_ocorrencia();




