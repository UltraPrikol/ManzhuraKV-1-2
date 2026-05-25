import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { GeoNote } from '../types';
import * as database from '../utils/database';

export const loadNotes = createAsyncThunk('notes/loadNotes', async () => {
    return await database.getNotes();
});

export const saveNote = createAsyncThunk('notes/saveNote', async (note: GeoNote) => {
    await database.addNote(note);
    return note;
});

export const removeNote = createAsyncThunk('notes/removeNote', async (id: string) => {
    await database.deleteNote(id);
    return id;
});

interface NotesState {
    items: GeoNote[];
    loading: boolean;
    error: string | null;
}

const initialState: NotesState = {
    items: [],
    loading: false,
    error: null
};

const notesSlice = createSlice({
    name: 'notes',
    initialState,
    reducers: {
        clearError: (state) => {
            state.error = null;
        }
    },
    extraReducers: (builder) => {
        builder
            // Загрузка
            .addCase(loadNotes.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(loadNotes.fulfilled, (state, action: PayloadAction<GeoNote[]>) => {
                state.loading = false;
                state.items = action.payload;
            })
            .addCase(loadNotes.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Ошибка загрузки';
            })
            // Сохранение
            .addCase(saveNote.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(saveNote.fulfilled, (state, action: PayloadAction<GeoNote>) => {
                state.loading = false;
                state.items.unshift(action.payload); // Добавляем в начало списка
            })
            .addCase(saveNote.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Ошибка сохранения';
            })
            // Удаление
            .addCase(removeNote.fulfilled, (state, action: PayloadAction<string>) => {
                state.items = state.items.filter(note => note.id !== action.payload);
            });
    }
});

export const { clearError } = notesSlice.actions;
export default notesSlice.reducer;