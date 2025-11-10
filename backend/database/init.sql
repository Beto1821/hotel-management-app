-- 1. Apaga o banco de dados se ele já existir (para começar do zero)
DROP DATABASE IF EXISTS `HOTEL_APP`;

-- 2. Cria o banco de dados novamente
CREATE DATABASE `HOTEL_APP`;

-- 3. ESSENCIAL: Seleciona o banco de dados para usar nos comandos seguintes
USE `HOTEL_APP`;

-- 4. Início do script de criação de tabelas (versão corrigida)

-- Desabilita a verificação de chaves estrangeiras
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

-- Criação da tabela de Quartos
CREATE TABLE IF NOT EXISTS `quartos` (
`id` INT NOT NULL AUTO_INCREMENT,
`numero` VARCHAR(10) NOT NULL,
`tipo` ENUM('standard', 'deluxe', 'suite') NOT NULL DEFAULT 'standard',
`status` ENUM('livre', 'ocupado', 'limpeza', 'manutencao') NOT NULL DEFAULT 'livre',
`capacidade` INT NOT NULL DEFAULT 2,
`valor_diaria` DECIMAL(10, 2) NOT NULL,
`descricao` TEXT NULL,
`created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`id`),
UNIQUE INDEX `numero_UNIQUE` (`numero` ASC) VISIBLE
)
ENGINE = InnoDB
COMMENT = 'Tabela para gerenciar os quartos do hotel.';


-- Criação da tabela de Clientes
CREATE TABLE IF NOT EXISTS `clientes` (
`id` INT NOT NULL AUTO_INCREMENT,
`nome_completo` VARCHAR(255) NOT NULL,
`email` VARCHAR(255) NOT NULL,
`telefone` VARCHAR(20) NULL,
`documento` VARCHAR(50) NOT NULL,
`endereco` VARCHAR(255) NULL,
`created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`id`),
UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
UNIQUE INDEX `documento_UNIQUE` (`documento` ASC) VISIBLE
)
ENGINE = InnoDB
COMMENT = 'Tabela para armazenar os dados dos clientes do hotel.';


-- Criação da tabela de Reservas
CREATE TABLE IF NOT EXISTS `reservas` (
`id` INT NOT NULL AUTO_INCREMENT,
`cliente_id` INT NOT NULL,
`quarto_id` INT NOT NULL,
`data_check_in` DATE NOT NULL,
`data_check_out` DATE NOT NULL,
`valor_total` DECIMAL(10, 2) NOT NULL,
`status` ENUM('pendente', 'ativa', 'concluida', 'cancelada') NOT NULL DEFAULT 'pendente',
`created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`id`),
INDEX `fk_reservas_clientes_idx` (`cliente_id` ASC) VISIBLE,
INDEX `fk_reservas_quartos_idx` (`quarto_id` ASC) VISIBLE,
CONSTRAINT `fk_reservas_clientes`
  FOREIGN KEY (`cliente_id`)
  REFERENCES `clientes` (`id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE,
CONSTRAINT `fk_reservas_quartos`
  FOREIGN KEY (`quarto_id`)
  REFERENCES `quartos` (`id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE
)
ENGINE = InnoDB
COMMENT = 'Tabela para gerenciar as reservas, ligando clientes e quartos.';

-- Habilita novamente a verificação de chaves estrangeiras
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;