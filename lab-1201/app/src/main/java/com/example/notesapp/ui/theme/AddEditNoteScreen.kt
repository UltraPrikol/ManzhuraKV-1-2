package com.example.notesapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddEditNoteScreen(
    onSaveClick: (String, String) -> Unit,
    onNavigateBack: () -> Unit,
    initialTitle: String = "",
    initialContent: String = ""
) {
    // Используем remember с ключами, чтобы поля обновлялись при загрузке старой заметки
    var title by remember(initialTitle) { mutableStateOf(initialTitle) }
    var content by remember(initialContent) { mutableStateOf(initialContent) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (initialTitle.isEmpty() && title.isEmpty()) "Новая заметка" else "Редактирование") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Text("<-") // Простая стрелка назад текстом
                    }
                },
                actions = {
                    TextButton(
                        onClick = {
                            if (title.isNotBlank() && content.isNotBlank()) {
                                onSaveClick(title, content)
                            }
                        },
                        enabled = title.isNotBlank() && content.isNotBlank()
                    ) {
                        Text("Сохранить")
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            OutlinedTextField(
                value = title,
                onValueChange = { title = it },
                label = { Text("Заголовок") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            OutlinedTextField(
                value = content,
                onValueChange = { content = it },
                label = { Text("Содержание") },
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
                minLines = 5
            )
        }
    }
}