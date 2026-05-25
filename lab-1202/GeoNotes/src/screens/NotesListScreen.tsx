import React, { useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useAppDispatch, useAppSelector } from '../hooks/reduxHooks';
import { loadNotes } from '../store/notesSlice';

export default function NotesListScreen({ navigation }: any) {
    const dispatch = useAppDispatch();
    const { items: notes, loading, error } = useAppSelector(state => state.notes);

    useEffect(() => {
        dispatch(loadNotes());
    }, [dispatch]);

    const renderNoteItem = ({ item }: any) => (
        <TouchableOpacity
            style={styles.noteItem}
            onPress={() => navigation.navigate('NoteDetail', { noteId: item.id })}
        >
            <View style={styles.noteHeader}>
                <Text style={styles.noteTitle}>{item.title}</Text>
                <Text style={styles.noteDate}>
                    {new Date(item.createdAt).toLocaleDateString()}
                </Text>
            </View>
            <Text style={styles.noteContent} numberOfLines={2}>{item.content}</Text>
            {item.address && <Text style={styles.noteAddress} numberOfLines={1}>📍 {item.address}</Text>}
            {item.photoUri && (
                <View style={styles.photoBadge}>
                    <Text style={styles.photoBadgeText}>📷</Text>
                </View>
            )}
        </TouchableOpacity>
    );

    if (loading && notes.length === 0) {
        return <View style={styles.center}><ActivityIndicator size="large" color="#007AFF" /></View>;
    }

    return (
        <View style={styles.container}>
            <FlatList
                data={notes}
                renderItem={renderNoteItem}
                keyExtractor={item => item.id}
                contentContainerStyle={styles.list}
                ListEmptyComponent={<Text style={styles.empty}>Нет заметок. Нажми +</Text>}
            />
            <TouchableOpacity style={styles.fab} onPress={() => navigation.navigate('AddNote')}>
                <Text style={styles.fabText}>+</Text>
            </TouchableOpacity>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f5f5f5' },
    center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
    list: { padding: 16 },
    empty: { textAlign: 'center', marginTop: 50, color: '#666' },
    noteItem: { backgroundColor: 'white', padding: 16, marginBottom: 12, borderRadius: 8, elevation: 3 },
    noteHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
    noteTitle: { fontSize: 16, fontWeight: 'bold', flex: 1 },
    noteDate: { fontSize: 12, color: '#666' },
    noteContent: { fontSize: 14, color: '#333', marginBottom: 8 },
    noteAddress: { fontSize: 12, color: '#007AFF' },
    photoBadge: { position: 'absolute', top: 16, right: 16, backgroundColor: '#007AFF', borderRadius: 12, paddingHorizontal: 6, paddingVertical: 2 },
    photoBadgeText: { color: 'white', fontSize: 10 },
    fab: { position: 'absolute', bottom: 24, right: 24, width: 56, height: 56, borderRadius: 28, backgroundColor: '#007AFF', justifyContent: 'center', alignItems: 'center', elevation: 8 },
    fabText: { fontSize: 24, color: 'white', fontWeight: 'bold' }
});