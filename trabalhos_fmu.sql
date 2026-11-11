-- Tabela de Clientes
CREATE TABLE IF NOT EXISTS Clientes (
    CodCliente TEXT PRIMARY KEY,
    NomeCliente TEXT NOT NULL
);

-- 2. Tabela de Produtos
CREATE TABLE IF NOT EXISTS Produtos (
    CodProduto TEXT PRIMARY KEY,
    NomeProduto TEXT NOT NULL,
    PrecoUnit REAL NOT NULL
);

-- 3. Tabela de Pedidos
CREATE TABLE IF NOT EXISTS Pedidos (
    Pedido INTEGER PRIMARY KEY,
    DataPedido TEXT NOT NULL,
    CodCliente TEXT NOT NULL,
    FOREIGN KEY (CodCliente) REFERENCES Clientes(CodCliente)
);

-- 4. Tabela de Itens do Pedido
CREATE TABLE IF NOT EXISTS Itens_Pedido (
    Pedido INTEGER NOT NULL,
    CodProduto TEXT NOT NULL,
    Qtd INTEGER NOT NULL,
    PRIMARY KEY (Pedido, CodProduto),
    FOREIGN KEY (Pedido) REFERENCES Pedidos(Pedido),
    FOREIGN KEY (CodProduto) REFERENCES Produtos(CodProduto)
);


-- Inserir dados de exemplo
INSERT OR IGNORE INTO Clientes (CodCliente, NomeCliente) VALUES 
('C01', 'Ana Lima'),
('C02', 'Bruno Alves');

INSERT OR IGNORE INTO Produtos (CodProduto, NomeProduto, PrecoUnit) VALUES 
('P10', 'Teclado', 120.00),
('P20', 'Mouse', 50.00);

INSERT OR IGNORE INTO Pedidos (Pedido, DataPedido, CodCliente) VALUES 
(1001, '2026-09-10', 'C01'),
(1002, '2026-09-12', 'C02');

INSERT OR IGNORE INTO Itens_Pedido (Pedido, CodProduto, Qtd) VALUES 
(1001, 'P10', 1),
(1001, 'P20', 2),
(1002, 'P10', 1);

-- Consulta unida (JOIN) para o relatório
SELECT 
    p.Pedido, 
    p.DataPedido, 
    c.CodCliente, 
    c.NomeCliente, 
    pr.CodProduto, 
    pr.NomeProduto, 
    i.Qtd, 
    pr.PrecoUnit
FROM Pedidos p
JOIN Clientes c ON p.CodCliente = c.CodCliente
JOIN Itens_Pedido i ON p.Pedido = i.Pedido
JOIN Produtos pr ON i.CodProduto = pr.CodProduto;