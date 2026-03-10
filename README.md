# Secure Cloud Storage

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red)](https://streamlit.io/)
[![Encryption](https://img.shields.io/badge/Encryption-AES--256-green)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
[![License](https://img.shields.io/badge/License-MIT-yellow)](#license)

A production-grade encrypted cloud storage system with **AES-256 encryption**, **distributed node architecture**, **Reed-Solomon erasure coding**, and **multi-user authentication**. Securely store and retrieve files with enterprise-level security.

## 🌟 Features

### 🔐 **Security Features**
- **AES-256 Encryption**: Military-grade encryption using CFB mode
- **SHA-256 Integrity Verification**: Generate and verify file hashes
- **Distributed Storage**: Files distributed across 4 virtual storage nodes
- **Reed-Solomon Erasure Coding**: Data redundancy and recovery capability
- **Secure Password Hashing**: SHA-256 hashed passwords in database

### 👤 **User Management**
- **Multi-User Support**: Individual accounts with isolated file storage
- **User Authentication**: Secure login and registration system
- **Session Management**: User sessions maintained across application
- **Private Storage**: Each user has isolated encrypted file storage

### 📁 **File Operations**
- **File Upload**: Encrypt and store files securely
- **File Download**: Download encrypted or decrypted files
- **Batch Download**: Select and download multiple files at once
- **File Deletion**: Securely delete files and associated metadata
- **Metadata Tracking**: Track upload timestamps and file names

### 📊 **System Architecture**
- **Chunked Storage**: Large files split into 20KB chunks
- **Distributed Nodes**: Chunks distributed across 4 nodes for redundancy
- **Cloud Dashboard**: Real-time security status and system overview
- **File Browser**: Interactive file management interface

## 🛠️ **Tech Stack**

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit (Python web framework) |
| **Backend** | Python 3.8+ |
| **Encryption** | cryptography (AES-256-CFB) |
| **Erasure Coding** | reedsolo (Reed-Solomon) |
| **Database** | MySQL Connector Python |
| **Storage** | Local filesystem (distributed nodes) |

## 📋 **Requirements**

```
streamlit>=1.0
cryptography>=41.0
reedsolo>=1.7
mysql-connector-python>=8.0
```

## 🚀 **Installation**

### Prerequisites
- Python 3.8 or higher
- MySQL server (XAMPP/MySQL Community Edition)
- pip (Python package manager)

### Step 1: Clone Repository
```bash
git clone https://github.com/Parani6379/Secure-cloud-storage.git
cd Secure-cloud-storage
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Database

#### Option A: Using XAMPP (Recommended)
1. Start MySQL via XAMPP Control Panel
2. Open phpMyAdmin at `http://localhost/phpmyadmin`
3. Create a new database called `secure_cloud`
4. Create users table with SQL:

```sql
CREATE DATABASE secure_cloud;
USE secure_cloud;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Option B: Using MySQL CLI
```bash
mysql -u root -p
```

```sql
CREATE DATABASE secure_cloud;
USE secure_cloud;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Step 5: Configure Database Connection

Edit `db.py` with your MySQL credentials:

```python
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      # Your MySQL password
        database="secure_cloud"
    )
```

### Step 6: Run Application
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 📖 **Usage Guide**

### First-Time User

#### 1. **Register Account**
- Click "Register" tab
- Enter username and password
- Click "Create Account"
- Account created successfully

#### 2. **Login**
- Click "Login" tab
- Enter username and password
- Click "Login"

#### 3. **Upload File**
- Navigate to "Upload Files" section
- Click "Choose a file"
- Select a file from your computer
- System automatically:
  - Splits file into 20KB chunks
  - Encrypts each chunk with AES-256
  - Applies Reed-Solomon erasure coding
  - Distributes across 4 storage nodes
  - Generates file hash for integrity
  - Stores metadata (filename, timestamp)
- Success message displays

#### 4. **View Files**
- Go to "My Files" section
- See list of all uploaded files
- View filenames and upload timestamps

#### 5. **Download File**
- Select file(s) with checkboxes
- Choose download option:
  - **Original**: Decrypted file (original format)
  - **Encrypted**: Encrypted binary file
- File downloads automatically

#### 6. **Delete File**
- Select file(s) with checkboxes
- Click "Delete Selected Files"
- Confirm action
- Files and associated data deleted permanently

### Dashboard
- View security features in use
- See encryption method (AES-256)
- Check integrity verification (SHA-256)
- Confirm distributed node storage

## 🏗️ **Architecture**

```
┌─────────────────────────────────────┐
│      Streamlit Web Interface        │
│  (Login, Upload, Download, Delete)  │
└────────────────┬────────────────────┘
                 │
        ┌────────▼──────────┐
        │   app.py (Main)   │
        │  - Authentication │
        │  - File Handling  │
        │  - UI Management  │
        └────────┬──────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌─────────┐  ┌─────────┐  ┌──────────────┐
│  auth   │  │ modules │  │   Storage    │
│ .py     │  │ folder  │  │  Nodes 1-4   │
│-Login   │  │-encrypt │  │-Encrypted    │
│-Register│  │-split   │  │ chunks       │
└─────────┘  │-erasure │  │-Metadata     │
             │ code    │  │-Hashes       │
             │-integrty│  └──────────────┘
             │-reconstruct
             └─────────┘
                 │
                 ▼
            ┌─────────┐
            │  MySQL  │
            │ Database│
            │ (users) │
            └─────────┘
```

## 📁 **Project Structure**

```
Secure-cloud-storage/
├── app.py                          # Main Streamlit application
├── auth.py                         # User authentication (login/register)
├── config.py                       # Configuration (chunk size, encryption key)
├── db.py                          # Database connection helper
├── requirements.txt               # Python dependencies
├── modules/                       # Core functionality modules
│   ├── encryption.py             # AES-256 encryption/decryption
│   ├── file_splitter.py          # Split files into chunks
│   ├── file_reconstructor.py     # Reconstruct from encrypted chunks
│   ├── erasure_coding.py         # Reed-Solomon error correction
│   ├── storage_manager.py        # Distributed node storage
│   └── integrity.py              # Hash generation & verification
├── user_files/                   # Runtime directory (created at startup)
│   └── {username}/               # Per-user directory
│       └── {file_id}/            # Per-file directory
│           ├── nodes/            # 4 distributed storage nodes
│           ├── encrypted.bin     # Full encrypted file
│           ├── file_hash.txt     # SHA-256 hash
│           └── metadata.json     # File metadata
└── .gitignore                    # Git ignore rules
```

## 🔐 **Security Implementation**

### Encryption Process
```
Original File
     │
     ▼
Split into 20KB Chunks
     │
     ▼
AES-256-CFB Encryption (per chunk)
     │
     ▼
Reed-Solomon Erasure Coding (10 parity blocks)
     │
     ▼
Distribute across 4 Virtual Nodes
     │
     ▼
Encrypted Storage + Metadata + Hash
```

### Decryption & Reconstruction
```
Load from Distributed Nodes
     │
     ▼
Reed-Solomon Decode (recover from erasure code)
     │
     ▼
AES-256-CFB Decryption
     │
     ▼
Reconstruct Original File
     │
     ▼
Verify Hash (SHA-256) Integrity
```

### Key Security Features
- **AES-256 in CFB Mode**: Symmetric encryption with random IV per encryption
- **Reed-Solomon (10,4)**: Can recover from loss of up to 4 blocks
- **SHA-256 Hashing**: Verify file integrity on download
- **Salted Password Hashing**: Passwords hashed with SHA-256
- **User Isolation**: Each user has isolated file storage

## ⚙️ **Configuration**

Edit `config.py` to customize:

```python
CHUNK_SIZE = 1024 * 20  # 20KB chunks
KEY = b'0123456789abcdef0123456789abcdef'  # 32-byte AES key
```

⚠️ **Warning**: Change the KEY value for production deployment.

## 💻 **API Modules**

### `encryption.py`
- `encrypt_data(data, key)` - Encrypt data with AES-256
- `decrypt_data(data, key)` - Decrypt AES-256 encrypted data

### `file_splitter.py`
- `split_file(data)` - Split file into chunks

### `erasure_coding.py`
- `encode_chunk(chunk)` - Reed-Solomon encode
- `decode_chunk(chunk)` - Reed-Solomon decode

### `storage_manager.py`
- `store_chunks(base_path, chunks)` - Distribute to nodes
- `load_chunks(base_path)` - Retrieve from nodes

### `file_reconstructor.py`
- `reconstruct(chunks)` - Decode and decrypt chunks

### `integrity.py`
- `generate_hash(data)` - Generate SHA-256 hash

### `auth.py`
- `register_user(username, password)` - Create new account
- `login_user(username, password)` - Authenticate user
- `hash_password(password)` - Hash password with SHA-256

## 🐛 **Troubleshooting**

### Issue: "MySQL connection error"
**Solution**: 
1. Ensure MySQL is running (XAMPP Control Panel → Start MySQL)
2. Verify database `secure_cloud` exists
3. Check credentials in `db.py`
4. Create users table if missing

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: 
```bash
pip install -r requirements.txt
```

### Issue: "Username already exists"
**Solution**: Use a different username during registration

### Issue: "File upload fails silently"
**Solution**:
1. Check write permissions in project directory
2. Ensure `user_files/` directory exists
3. Check available disk space

### Issue: "Download button doesn't work"
**Solution**:
1. Verify file was uploaded successfully
2. Check user_files directory for file data
3. Ensure encryption.bin and chunks exist

## 🔄 **Workflow Example**

```
1. User registers: "john" / "password123"
   └─ MySQL: user (john, sha256_hash) inserted

2. User uploads: document.pdf (5MB)
   └─ Split: 250 chunks of 20KB
   └─ Encrypt: AES-256-CFB each chunk
   └─ Encode: Reed-Solomon (10 parity)
   └─ Store: Chunks distributed to nodes/node1-4
   └─ Hash: SHA-256 of original file
   └─ Metadata: filename, timestamp

3. User downloads: select document.pdf
   └─ Load chunks from distributed nodes
   └─ Decode: Reed-Solomon recovery
   └─ Decrypt: AES-256-CFB
   └─ Reconstruct: Original file
   └─ Verify: Hash matches stored hash
   └─ Download: As original or encrypted

4. User deletes: document.pdf
   └─ Remove all chunks from nodes
   └─ Delete metadata and hash
   └─ Remove file_id directory
```

## 📊 **Performance Metrics**

| Metric | Value |
|--------|-------|
| **Chunk Size** | 20 KB |
| **Encryption** | AES-256 (CFB mode) |
| **Erasure Code** | Reed-Solomon (10,4) |
| **Storage Nodes** | 4 (virtual) |
| **Hash Algorithm** | SHA-256 |
| **Max File Size** | Limited by disk space |

## 🚀 **Future Enhancements**

- [ ] Actual distributed node network (remote servers)
- [ ] Database-backed storage instead of filesystem
- [ ] File sharing with encryption key management
- [ ] Automatic backup to cloud providers
- [ ] REST API for programmatic access
- [ ] Web-based file preview (images, documents)
- [ ] Real-time file sync across devices
- [ ] Audit logging and activity tracking
- [ ] Two-factor authentication (2FA)
- [ ] S3/Cloud provider integration

## 📄 **License**

This project is open source and available under the MIT License.

## 🤝 **Contributing**

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 **Support**

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Repository**: [Parani6379/Secure-cloud-storage](https://github.com/Parani6379/Secure-cloud-storage)  
**Last Updated**: March 10, 2026  
**Language**: Python 3.8+
