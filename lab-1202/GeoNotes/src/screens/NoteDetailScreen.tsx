import React from 'react';
import { View, Text, StyleSheet, ScrollView, Image, TouchableOpacity, Alert } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import { useAppDispatch, useAppSelector } from '../hooks/reduxHooks';
import { removeNote } from '../store/notesSlice';

export default function NoteDetailScreen({ navigation, route }: any) {
    const { noteId } = route.params;
    const dispatch = useAppDispatch();
    const note = useAppSelector(state => state.notes.items.find(item => item.id === noteId));

    if (!note) return null;

    const handleDelete = () => {
        Alert.alert('Удаление', 'Удалить заметку?', [
            { text: 'Отмена', style: 'cancel' },
            {
                text: 'Удалить', style: 'destructive',
                onPress: async () => {
                    await dispatch(removeNote(noteId)).unwrap();
                    navigation.goBack();
                }
            }
        ]);
    };

    return (
        <ScrollView style={styles.container}>
            <View style={styles.card}>
                <Text style={styles.title}>{note.title}</Text>
                <Text style={styles.date}>{new Date(note.createdAt).toLocaleString()}</Text>
                <Text style={styles.content}>{note.content}</Text>
                {note.address && <Text style={styles.address}>📍 {note.address}</Text>}
            </View>

            <View style={styles.mapContainer}>
                <MapView
                    style={styles.map}
                    initialRegion={{ latitude: note.latitude, longitude: note.longitude, latitudeDelta: 0.01, longitudeDelta: 0.01 }}
                >
                    <Marker coordinate={{ latitude: note.latitude, longitude: note.longitude }} />
                </MapView>
            </View>

            {note.photoUri && <Image source={{ uri: note.photoUri }} style={styles.photo} />}

            <TouchableOpacity style={styles.deleteBtn} onPress={handleDelete}>
                <Text style={styles.deleteText}>Удалить заметку</Text>
            </TouchableOpacity>
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f5f5f5' },
    card: { backgroundColor: 'white', padding: 20, marginBottom: 8 },
    title: { fontSize: 24, fontWeight: 'bold', marginBottom: 8 },
    date: { color: '#666', marginBottom: 12 },
    content: { fontSize: 16, lineHeight: 24, marginBottom: 12 },
    address: { color: '#007AFF' },
    mapContainer: { height: 200, marginBottom: 8 },
    map: { flex: 1 },
    photo: { width: '100%', height: 250, marginBottom: 8, resizeMode: 'cover' },
    deleteBtn: { backgroundColor: '#ff3b30', margin: 20, padding: 16, borderRadius: 8, alignItems: 'center' },
    deleteText: { color: 'white', fontWeight: 'bold' }
});