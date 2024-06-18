--Garantir a unicidade da combinação de produto_id e propriedade_id em core_estoque
ALTER TABLE core_estoque
ADD CONSTRAINT produto_propriedade_unique UNIQUE (produto_id, propriedade_id);

--------------------------------------------------------------------------------------------------

--COMPONENTE COMPRA DE PRODUTO

-- Função para atualizar o estoque após o INSERT da compra
CREATE OR REPLACE FUNCTION trigger_inserir_compraproduto() RETURNS TRIGGER AS $$
BEGIN
	INSERT INTO core_estoque (produto_id, propriedade_id, quantidade)
    VALUES (NEW.produto_id, NEW.propriedade_id, NEW."quantidadeComprada")
    ON CONFLICT (produto_id, propriedade_id)
    DO UPDATE SET quantidade = core_estoque.quantidade + NEW."quantidadeComprada";
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o INSERT
CREATE TRIGGER apos_inserir_compra
AFTER INSERT ON core_compraproduto
FOR EACH ROW
EXECUTE FUNCTION trigger_inserir_compraproduto();


-- Função para atualizar o estoque após o DELETE da compra
CREATE OR REPLACE FUNCTION trigger_excluir_compraproduto() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_estoque
    SET quantidade = quantidade - OLD."quantidadeComprada"
    WHERE produto_id = OLD.produto_id AND propriedade_id = OLD.propriedade_id;
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o DELETE
CREATE TRIGGER apos_excluir_compra
AFTER DELETE ON core_compraproduto
FOR EACH ROW
EXECUTE FUNCTION trigger_excluir_compraproduto();


--Função para atualizar o estoque após o UPDATE da compra
CREATE OR REPLACE FUNCTION trigger_atualizar_compraproduto() RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se o produto_id foi alterado
    IF OLD.produto_id IS DISTINCT FROM NEW.produto_id THEN
        -- Atualiza estoque do produto antigo
        UPDATE core_estoque
        SET quantidade = quantidade - OLD."quantidadeComprada"
    	WHERE produto_id = OLD.produto_id AND propriedade_id = OLD.propriedade_id;
        
        -- Atualiza o estoque do produto novo
        INSERT INTO core_estoque (produto_id, propriedade_id, quantidade)
		VALUES (NEW.produto_id, NEW.propriedade_id, NEW."quantidadeComprada")
		ON CONFLICT (produto_id, propriedade_id)
		DO UPDATE SET quantidade = core_estoque.quantidade + NEW."quantidadeComprada";
    END IF;

    -- Verifica se a quantidade foi alterada
    IF OLD."quantidadeComprada" IS DISTINCT FROM NEW."quantidadeComprada" THEN
        -- Atualiza quantidade do estoque
        UPDATE core_estoque
        SET quantidade = quantidade - OLD."quantidadeComprada" + NEW."quantidadeComprada"
        WHERE produto_id = NEW.produto_id AND propriedade_id = NEW.propriedade_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o UPDATE
CREATE TRIGGER apos_atualizar_compra
AFTER UPDATE ON core_compraproduto
FOR EACH ROW
EXECUTE FUNCTION trigger_atualizar_compraproduto();


---------------------------------------------------------------------------------------------
--COMPONENTE SUPLEMENTAÇÃO

-- Função para atualizar o estoque após o INSERT da suplementacao
CREATE OR REPLACE FUNCTION trigger_inserir_suplementacao()
RETURNS TRIGGER AS $$
DECLARE
    v_propriedade_id INT;
BEGIN
    -- Recuperar o propriedade_id usando o piquete_id
    SELECT pq.propriedade_id
    INTO v_propriedade_id
    FROM core_piquete AS pq
    WHERE pq.id = NEW.piquete_id
    LIMIT 1;
    
    -- Inserir ou atualizar na tabela core_estoque
    INSERT INTO core_estoque (produto_id, propriedade_id, quantidade)
    VALUES (NEW.produto_id, v_propriedade_id, -NEW.quantidade)
    ON CONFLICT (produto_id, propriedade_id)
    DO UPDATE SET quantidade = core_estoque.quantidade - NEW.quantidade;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o INSERT
CREATE TRIGGER apos_inserir_suplementacao
AFTER INSERT ON core_suplementacao
FOR EACH ROW
EXECUTE FUNCTION trigger_inserir_suplementacao();


-- Função para atualizar o estoque após o DELETE da suplementação
CREATE OR REPLACE FUNCTION trigger_excluir_suplementacao() RETURNS TRIGGER AS $$
DECLARE
    v_propriedade_id INT;
BEGIN
	-- Recuperar o propriedade_id usando o piquete_id
    SELECT pq.propriedade_id
    INTO v_propriedade_id
    FROM core_piquete AS pq
    WHERE pq.id = OLD.piquete_id
    LIMIT 1;

    UPDATE core_estoque
    SET quantidade = quantidade + OLD.quantidade
    WHERE produto_id = OLD.produto_id AND propriedade_id = v_propriedade_id;
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o DELETE
CREATE TRIGGER apos_excluir_suplementacao
AFTER DELETE ON core_suplementacao
FOR EACH ROW
EXECUTE FUNCTION trigger_excluir_suplementacao();


CREATE OR REPLACE FUNCTION trigger_atualizar_suplementacao() RETURNS TRIGGER AS $$
DECLARE
    v_propriedade_id INT;
BEGIN
	-- Recuperar o propriedade_id usando o piquete_id
    SELECT pq.propriedade_id
    INTO v_propriedade_id
    FROM core_piquete AS pq
    WHERE pq.id = NEW.piquete_id
    LIMIT 1;
	
    -- Verifica se o produto_id foi alterado
    IF (OLD.produto_id IS DISTINCT FROM NEW.produto_id) THEN
        -- Atualiza estoque do produto antigo
        UPDATE core_estoque
        SET quantidade = quantidade + OLD.quantidade
    	WHERE produto_id = OLD.produto_id AND propriedade_id = v_propriedade_id;
        
        -- Atualiza o estoque do produto novo
        INSERT INTO core_estoque (produto_id, propriedade_id, quantidade)
		VALUES (NEW.produto_id, v_propriedade_id, -NEW.quantidade)
		ON CONFLICT (produto_id, propriedade_id)
		DO UPDATE SET quantidade = core_estoque.quantidade - NEW.quantidade; 
    END IF;

    -- Verifica se a quantidade foi alterada
    IF (OLD.quantidade IS DISTINCT FROM NEW.quantidade) THEN
        -- Atualiza quantidade do estoque
        UPDATE core_estoque
        SET quantidade = quantidade + OLD.quantidade - NEW.quantidade
        WHERE produto_id = NEW.produto_id AND propriedade_id = v_propriedade_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o UPDATE
CREATE TRIGGER apos_atualizar_suplementacao
AFTER UPDATE ON core_suplementacao
FOR EACH ROW
EXECUTE FUNCTION trigger_atualizar_suplementacao();


--------------------------------------------------------------------------------------------------
-- COMPONENTE APLICACAO DE PRODUTOS

-- Função para atualizar o estoque após o INSERT da aplicacaoProdutos
CREATE OR REPLACE FUNCTION trigger_inserir_aplicacaoproduto() RETURNS TRIGGER AS $$
DECLARE
    v_propriedade_id INT;
BEGIN
    -- Recuperar o propriedade_id usando o animal_id
    SELECT pq.propriedade_id
    INTO v_propriedade_id
    FROM core_piquete AS pq
    JOIN core_animal AS a ON a.piquete_id = pq.id
    WHERE a.id = NEW.animal_id
    LIMIT 1;
    
    -- Inserir ou atualizar na tabela core_estoque
    INSERT INTO core_estoque (produto_id, propriedade_id, quantidade)
    VALUES (NEW.produto_id, v_propriedade_id, - NEW.dosagem)
    ON CONFLICT (produto_id, propriedade_id)
    DO UPDATE SET quantidade = core_estoque.quantidade - NEW.dosagem;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o INSERT
CREATE TRIGGER apos_inserir_aplicacao
AFTER INSERT ON core_aplicacaoproduto
FOR EACH ROW
EXECUTE FUNCTION trigger_inserir_aplicacaoproduto();


-- Função para atualizar o estoque após o DELETE da aplicacaoProdutos
CREATE OR REPLACE FUNCTION trigger_excluir_aplicacaoproduto() RETURNS TRIGGER AS $$
DECLARE
    v_propriedade_id INT;
BEGIN
    -- Recuperar o propriedade_id usando o animal_id
    SELECT pq.propriedade_id
    INTO v_propriedade_id
    FROM core_piquete AS pq
    JOIN core_animal AS a ON a.piquete_id = pq.id
    WHERE a.id = OLD.animal_id
    LIMIT 1;

    UPDATE core_estoque
    SET quantidade = quantidade + OLD.dosagem
    WHERE produto_id = OLD.produto_id AND propriedade_id = v_propriedade_id;
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o DELETE
CREATE TRIGGER apos_excluir_aplicacao
AFTER DELETE ON core_aplicacaoproduto
FOR EACH ROW
EXECUTE FUNCTION trigger_excluir_aplicacaoproduto();


-- Função para atualizar o estoque após o UPDATE da aplicacaoProdutos
CREATE OR REPLACE FUNCTION trigger_atualizar_aplicacaoproduto() RETURNS TRIGGER AS $$
DECLARE
    v_propriedade_id INT;
BEGIN
    -- Recuperar o propriedade_id usando o animal_id
    SELECT pq.propriedade_id
    INTO v_propriedade_id
    FROM core_piquete AS pq
    JOIN core_animal AS a ON a.piquete_id = pq.id
    WHERE a.id = NEW.animal_id
    LIMIT 1;
	
    -- Verifica se o produto_id foi alterado
    IF (OLD.produto_id IS DISTINCT FROM NEW.produto_id) THEN
        -- Atualiza estoque do produto antigo
        UPDATE core_estoque
        SET quantidade = quantidade + OLD.dosagem
    	WHERE produto_id = OLD.produto_id AND propriedade_id = v_propriedade_id;
        
        -- Atualiza o estoque do produto novo
        INSERT INTO core_estoque (produto_id, propriedade_id, quantidade)
		VALUES (NEW.produto_id, v_propriedade_id, - NEW.dosagem)
		ON CONFLICT (produto_id, propriedade_id)
		DO UPDATE SET quantidade = core_estoque.quantidade - NEW.dosagem; 
    END IF;

    -- Verifica se a dosagem foi alterada
    IF (OLD.dosagem IS DISTINCT FROM NEW.dosagem) THEN
        -- Atualiza quantidade do estoque
        UPDATE core_estoque
        SET quantidade = quantidade + OLD.dosagem - NEW.dosagem
        WHERE produto_id = NEW.produto_id AND propriedade_id = v_propriedade_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o UPDATE
CREATE TRIGGER apos_atualizar_aplicacao
AFTER UPDATE ON core_aplicacaoproduto
FOR EACH ROW
EXECUTE FUNCTION trigger_atualizar_aplicacaoproduto();

----------------------------------------------------------------------------------------------------

--COMPONENTE VENDA DE ANIMAIS

-- Função para atualizar o status do animal após o insert da venda
CREATE OR REPLACE FUNCTION trigger_inserir_vendaanimal() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_animal
    SET status = 'Vendido', "dataBaixa" = NEW."dataVenda"
    WHERE id = NEW.animal_id;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o insert
CREATE TRIGGER apos_inserir_vendaanimal
AFTER INSERT ON core_vendaanimal
FOR EACH ROW
EXECUTE FUNCTION trigger_inserir_vendaanimal();


-- Função para atualizar o status do animal após o delete da venda
CREATE OR REPLACE FUNCTION trigger_excluir_vendaanimal() RETURNS TRIGGER AS $$
BEGIN
    UPDATE core_animal
    SET status = 'Vivo', "dataBaixa" = NULL
    WHERE id = OLD.animal_id;
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o delete
CREATE TRIGGER apos_excluir_vendaanimal
AFTER DELETE ON core_vendaanimal
FOR EACH ROW
EXECUTE FUNCTION trigger_excluir_vendaanimal();


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

-- Trigger que dispara após o update
CREATE TRIGGER apos_atualizar_vendaanimal
AFTER UPDATE ON core_vendaanimal
FOR EACH ROW
EXECUTE FUNCTION trigger_atualizar_vendaanimal();

---------------------------------------------------------------------------------------------------

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

-- Trigger que dispara após o insert
CREATE TRIGGER apos_inserir_ocorrencia
AFTER INSERT ON core_ocorrencia
FOR EACH ROW
EXECUTE FUNCTION trigger_inserir_ocorrencia();


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

-- Trigger que dispara após o delete
CREATE TRIGGER apos_excluir_ocorrencia
AFTER DELETE ON core_ocorrencia
FOR EACH ROW
EXECUTE FUNCTION trigger_excluir_ocorrencia();


-- Função para atualizar o status do animal após o update da ocorrencia
CREATE OR REPLACE FUNCTION trigger_atualizar_ocorrencia() RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se o tipo da ocorrencia foi alterado de morte para outra coisa
    IF OLD.tipo = 'Morte' AND NEW.tipo !='Morte' THEN
        -- Atualiza status do animal
        UPDATE core_animal
        SET status = 'Vivo', "dataBaixa" = NULL
        WHERE id = OLD.animal_id;
    END IF;
	
	-- Verifica se o tipo da ocorrencia foi alterado de outra coisa para morte
    IF OLD.tipo != 'Morte' AND NEW.tipo ='Morte' THEN
        -- Atualiza status do animal
        UPDATE core_animal
        SET status = 'Morto', "dataBaixa" = NEW."dataOcorrencia"
        WHERE id = OLD.animal_id;
    END IF;

    -- Verifica se a data de ocorrencia foi alterada
    IF OLD."dataOcorrencia" IS DISTINCT FROM NEW."dataOcorrencia" AND NEW.tipo = 'Morte' THEN
        -- Atualiza dataBaixa
        UPDATE core_animal
        SET "dataBaixa" = NEW."dataOcorrencia"
        WHERE id = NEW.animal_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o update
CREATE TRIGGER apos_atualizar_ocorrencia
AFTER UPDATE ON core_ocorrencia
FOR EACH ROW
EXECUTE FUNCTION trigger_atualizar_ocorrencia();


----------------------------------------------------------------------------------------------------------------

--COMPONENTE MOVIMENTAÇÃO

-- Função para atualizar o piquete do animal após o INSERT da Movimentacao
CREATE OR REPLACE FUNCTION trigger_inserir_movimentacao() RETURNS TRIGGER AS $$
BEGIN
	UPDATE core_animal
	SET piquete_id = NEW."piqueteDestino_id"
	WHERE id = NEW.animal_id;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o INSERT
CREATE TRIGGER apos_inserir_movimentacao
AFTER INSERT ON core_movimentacao
FOR EACH ROW
EXECUTE FUNCTION trigger_inserir_movimentacao();


-- Função para atualizar o piquete do animal após o DELETE da movimentacao
CREATE OR REPLACE FUNCTION trigger_excluir_movimentacao() RETURNS TRIGGER AS $$
BEGIN
	UPDATE core_animal
	SET piquete_id = OLD."piqueteOrigem_id"
	WHERE id = OLD.animal_id;
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger que dispara após o delete
CREATE TRIGGER apos_excluir_movimentacao
AFTER DELETE ON core_movimentacao
FOR EACH ROW
EXECUTE FUNCTION trigger_excluir_movimentacao();