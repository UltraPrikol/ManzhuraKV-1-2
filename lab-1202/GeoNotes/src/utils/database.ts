import * as SQLite from 'expo-sqlite';
import { GeoNote } from '../types';

const db = SQLite.openDatabaseSync('geonotes.db');

export const initDatabase = async (): Promise<void> => {
    try {
        db.execSync(`
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                address TEXT,
                photoUri TEXT,
                createdAt INTEGER NOT NULL
            );
        `);
        console.log('Database initialized');
    } catch (error) {
        console.error('Database initialization error:', error);
        throw error;
    }
};

export const getNotes = (): Promise<GeoNote[]> => {
    return new Promise((resolve) => {
        try {
            const allRows = db.getAllSync<GeoNote>('SELECT * FROM notes ORDER BY createdAt DESC');
            resolve(allRows || []);
        } catch (e) {
            resolve([]); 
        }
    });
};

export const addNote = (note: GeoNote): Promise<void> => {
    return new Promise((resolve, reject) => {
        try {
            db.runSync(
                'INSERT INTO notes (id, title, content, latitude, longitude, address, photoUri, createdAt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                [note.id, note.title, note.content, note.latitude, note.longitude, note.address || null, note.photoUri || null, note.createdAt]
            );
            resolve();
        } catch (error) {
            console.error('Add note error:', error);
            reject(error);
        }
    });
};

export const deleteNote = (id: string): Promise<void> => {
    return new Promise((resolve, reject) => {
        try {
            db.runSync('DELETE FROM notes WHERE id = ?', [id]);
            resolve();
        } catch (error) {
            console.error('Delete note error:', error);
            reject(error);
        }
    });
};

export const updateNote = (note: GeoNote): Promise<void> => {
    return new Promise((resolve, reject) => {
        try {
            db.runSync(
                'UPDATE notes SET title = ?, content = ?, address = ?, photoUri = ? WHERE id = ?',
                [note.title, note.content, note.address || null, note.photoUri || null, note.id]
            );
            resolve();
        } catch (error) {
            console.error('Update note error:', error);
            reject(error);
        }
    });
};