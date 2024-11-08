CREATE TABLE users (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  username TEXT NOT NULL UNIQUE, -- Nueva columna para el nombre de usuario
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password VARCHAR(60) NOT NULL, -- Columna para almacenar el hash de la contraseña
  device TEXT CHECK (device IN ('desktop', 'mobile')) NOT NULL
);

-- Inserciones de prueba con nombres de usuario y contraseñas hasheadas
INSERT INTO users (username, first_name, last_name, email, password, device)
VALUES
  ('johndoe', 'John', 'Doe', 'john.doe@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'desktop'),
  ('janesmith', 'Jane', 'Smith', 'jane.smith@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'mobile'),
  ('alicejohnson', 'Alice', 'Johnson', 'alice.johnson@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'desktop'),
  ('bobbrown', 'Bob', 'Brown', 'bob.brown@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'mobile'),
  ('charliedavis', 'Charlie', 'Davis', 'charlie.davis@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'desktop'),
  ('dianamiller', 'Diana', 'Miller', 'diana.miller@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'mobile'),
  ('evewilson', 'Eve', 'Wilson', 'eve.wilson@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'desktop'),
  ('frankmoore', 'Frank', 'Moore', 'frank.moore@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'mobile'),
  ('gracetaylor', 'Grace', 'Taylor', 'grace.taylor@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'desktop'),
  ('hankanderson', 'Hank', 'Anderson', 'hank.anderson@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'mobile'),
  ('ivythomas', 'Ivy', 'Thomas', 'ivy.thomas@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'desktop'),
  ('jackjackson', 'Jack', 'Jackson', 'jack.jackson@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'mobile'),
  ('karawhite', 'Kara', 'White', 'kara.white@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'desktop'),
  ('leoharris', 'Leo', 'Harris', 'leo.harris@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'mobile'),
  ('miamartin', 'Mia', 'Martin', 'mia.martin@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'desktop'),
  ('ninathompson', 'Nina', 'Thompson', 'nina.thompson@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'mobile'),
  ('oscargarcia', 'Oscar', 'Garcia', 'oscar.garcia@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'desktop'),
  ('paulmartinez', 'Paul', 'Martinez', 'paul.martinez@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'mobile'),
  ('quinnrobinson', 'Quinn', 'Robinson', 'quinn.robinson@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'desktop'),
  ('ritaclark', 'Rita', 'Clark', 'rita.clark@example.com', '$2b$12$KMH5iWSHe..SDFdkjnasfnRhhWmHx1.x23', 'mobile');
