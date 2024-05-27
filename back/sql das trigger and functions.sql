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