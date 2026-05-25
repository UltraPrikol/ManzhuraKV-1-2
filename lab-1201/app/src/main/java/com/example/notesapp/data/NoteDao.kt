package com.example.notesapp.data

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
@JvmSuppressWildcards
interface NoteDao {

    @Query("SELECT * FROM notes ORDER BY id DESC")
    fun getAllNotes(): Flow<List<Note>>

    // Возвращаем Long (ID новой строки)
    @Insert
    suspend fun insertNote(note: Note): Long

    // Возвращаем Int (кол-во обновленных строк)
    @Update
    suspend fun updateNote(note: Note): Int

    // Возвращаем Int (кол-во удаленных строк)
    @Delete
    suspend fun deleteNote(note: Note): Int

    @Query("SELECT * FROM notes WHERE id = :id")
    suspend fun getNoteById(id: Int): Note?
}