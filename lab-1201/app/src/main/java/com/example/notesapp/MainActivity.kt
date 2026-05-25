package com.example.notesapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.*
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.notesapp.data.NoteDatabase
import com.example.notesapp.data.NoteRepository
import com.example.notesapp.ui.AddEditNoteScreen
import com.example.notesapp.ui.NotesScreen
import com.example.notesapp.ui.NotesViewModel
import com.example.notesapp.ui.NotesViewModelFactory
import com.example.notesapp.ui.theme.NotesAppTheme

class MainActivity : ComponentActivity() {

    private lateinit var noteRepository: NoteRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val database = NoteDatabase.getDatabase(this)
        noteRepository = NoteRepository(database.noteDao())

        setContent {
            NotesAppTheme {
                NotesApp(noteRepository)
            }
        }
    }
}

@Composable
fun NotesApp(noteRepository: NoteRepository) {
    val navController = rememberNavController()
    // Создаем единую ViewModel для всего приложения
    val viewModel: NotesViewModel = viewModel(factory = NotesViewModelFactory(noteRepository))

    NavHost(
        navController = navController,
        startDestination = "notes_list"
    ) {
        composable("notes_list") {
            NotesScreen(
                viewModel = viewModel,
                onNoteClick = { noteId ->
                    // Переход на экран редактирования
                    navController.navigate("add_edit_note/$noteId")
                },
                onAddClick = {
                    // Переход на экран создания (-1 означает новую заметку)
                    navController.navigate("add_edit_note/-1")
                }
            )
        }

        composable("add_edit_note/{noteId}") { backStackEntry ->
            val noteIdStr = backStackEntry.arguments?.getString("noteId") ?: "-1"
            val noteId = noteIdStr.toIntOrNull() ?: -1

            // Если это редактирование, загружаем данные заметки
            LaunchedEffect(noteId) {
                if (noteId != -1) {
                    viewModel.loadNoteById(noteId)
                }
            }

            // Наблюдаем за текущей загруженной заметкой
            val currentNote by viewModel.currentNote.collectAsState()

            AddEditNoteScreen(
                initialTitle = if (noteId == -1) "" else (currentNote?.title ?: ""),
                initialContent = if (noteId == -1) "" else (currentNote?.content ?: ""),
                onSaveClick = { title, content ->
                    if (noteId == -1) {
                        viewModel.addNote(title, content)
                    } else {
                        viewModel.updateNote(noteId, title, content)
                    }
                    navController.popBackStack()
                },
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }
    }
}