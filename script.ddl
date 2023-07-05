-- Model: Django Models

CREATE TABLE User (
    id INT PRIMARY KEY,
    username VARCHAR2(30) NOT NULL,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(254) NOT NULL,
    is_staff NUMBER(1) DEFAULT 0 NOT NULL,
    is_active NUMBER(1) DEFAULT 1 NOT NULL,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE Cliente (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    rut VARCHAR2(10) NOT NULL,
    sexo VARCHAR2(10) NOT NULL,
    CONSTRAINT fk_cliente_user FOREIGN KEY (user_id) REFERENCES User (id)
);

CREATE TABLE Reserva (
    id INT PRIMARY KEY,
    cliente_id INT NOT NULL,
    agenda_id INT NOT NULL,
    dia DATE NOT NULL,
    confirmada NUMBER(1) DEFAULT 0 NOT NULL,
    CONSTRAINT fk_reserva_cliente FOREIGN KEY (cliente_id) REFERENCES Cliente (id),
    CONSTRAINT fk_reserva_agenda FOREIGN KEY (agenda_id) REFERENCES Agenda (id)
);

CREATE TABLE Boleta (
    id INT PRIMARY KEY,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    cliente_id INT NOT NULL,
    reserva_id INT NOT NULL,
    CONSTRAINT fk_boleta_cliente FOREIGN KEY (cliente_id) REFERENCES Cliente (id),
    CONSTRAINT fk_boleta_reserva FOREIGN KEY (reserva_id) REFERENCES Reserva (id)
);

CREATE TABLE TipoCancha (
    id INT PRIMARY KEY,
    nombre VARCHAR2(50) NOT NULL,
    precio NUMBER(8, 0) NOT NULL,
    descripcion CLOB NOT NULL
);

CREATE TABLE Cancha (
    id INT PRIMARY KEY,
    numeracion VARCHAR2(10) NOT NULL,
    tipo_id INT NOT NULL,
    CONSTRAINT fk_cancha_tipo FOREIGN KEY (tipo_id) REFERENCES TipoCancha (id)
);

CREATE TABLE Horario (
    id INT PRIMARY KEY,
    horario VARCHAR2(10) NOT NULL
);

CREATE TABLE Agenda (
    id INT PRIMARY KEY,
    cancha_id INT NOT NULL,
    horario_id INT NOT NULL,
    disponible NUMBER(1) DEFAULT 1 NOT NULL,
    CONSTRAINT fk_agenda_cancha FOREIGN KEY (cancha_id) REFERENCES Cancha (id),
    CONSTRAINT fk_agenda_horario FOREIGN KEY (horario_id) REFERENCES Horario (id)
);
