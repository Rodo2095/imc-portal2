# imc-portal
Nombre del Proyecto: Cálculo Web de IMC
Portal IMC y Gestión de Especialistas

Este proyecto es una aplicación web modular que permite a los usuarios calcular su Índice de Masa Corporal (IMC) y a los especialistas ver los datos de sus pacientes asignados automáticamente, adicional hay un portal de administradores que permite el acceso para realizar consultas en SQL. Está dividido en 3 portales independientes, completamente dockerizados y conectados a una base de datos PostgreSQL.

---

Objetivo

Desarrollar un sistema web dividido en dos módulos:
- **Portal de Clientes**: registro, login, cálculo de IMC y almacenamiento de historial.
- **Portal de Especialistas**: login y visualización de pacientes asignados en orden rotativo.
- **Portal de Administradores**: login y realiza consulta en SQL a la base de datos.

---

Tecnologías utilizadas

| Componente         | Tecnología / Paquete               | Propósito                                                               |
|---------------------|----------------------------------|-------------------------------------------------------|
| **Backend**          | Flask (Python)                          | Crear APIs REST para clientes y especialistas          |
|                               | SQLAlchemy                            | ORM para manejar la base de datos                       |
|                               | Flask-JWT / Flask-Login          | Autenticación de usuarios                                        |
|                               | Flask-Migrate                           | Migraciones de base de datos                                |
|                               | psycopg2                                 | Conexión con PostgreSQL                                       |
| **Base de datos**  | PostgreSQL                              | Almacenamiento de usuarios, IMC y asignaciones |
| **Frontend**          | HTML + Bootstrap  | Interfaces básicas para formularios                        |
| **Contenedores**  | Docker + Docker Compose     | Empaquetar y levantar los servicios                        |
| **Gestión**            | GitHub + GitHub Projects        | Control de versiones y tablero KANBAN                |
| **IDE**                   | Visual Studio Code                   | Edición de código                                                   |
| **Sistema**            | Kubuntu (VirtualBox)                | Entorno de desarrollo local                                    |

---

## 🚀 Cómo ejecutar el proyecto

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/imc-portal2.git
   cd imc-portal2


