-- -----------------------------------------------------
-- Tabela `Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Usuario` (
  `nome` VARCHAR(100) NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user`),
  
  );

-- -----------------------------------------------------
-- Tabela `post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `post` (
  `id_post`  PRIMARY KEY  AUTOINCREMENT,
  `TAG_post` VARCHAR(100) NOT NULL,
  `data_post` VARCHAR(10),
  `horario_post` DATETIME,
  `conteudo_post` VARCHAR(500) NOT NULL,
  `comentario_post` VARCHAR(500) NOT NULL,
  `estrelas_post` FLOAT,
  `Usuario_user` VARCHAR(45) NOT NULL,
  FOREIGN KEY (`Usuario_user`) REFERENCES `Usuario` (`user`)

);
