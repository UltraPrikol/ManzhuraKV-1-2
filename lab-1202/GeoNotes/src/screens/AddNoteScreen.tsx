import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, StyleSheet, TouchableOpacity, ScrollView, Alert, ActivityIndicator, Image } from 'react-native';
import * as Location from 'expo-location';
import * as ImagePicker from 'expo-image-picker';
import { useAppDispatch } from '../hooks/reduxHooks';
import { saveNote } from '../store/notesSlice';
import { GeoNote } from '../types';
import 'react-native-get-random-values';
import { v4 as uuidv4 } from 'uuid';

export default function AddNoteScreen({ navigation }: any) {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [address, setAddress] = useState<string | undefined>();
    const [photoUri, setPhotoUri] = useState<string | undefined>();
    const [isLoadingLoc, setIsLoadingLoc] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [location, setLocation] = useState<{ latitude: number; longitude: number } | null>(null);
    
    const dispatch = useAppDispatch();

    useEffect(() => {
        getCurrentLocation();
    }, []);

const getCurrentLocation = async () => {
    setIsLoadingLoc(true);

    try {
        const { status } = await Location.requestForegroundPermissionsAsync();

        if (status !== 'granted') {
            Alert.alert('Ошибка', 'Разрешение на геолокацию не выдано');
            return;
        }

        // Сначала проверяем включена ли геолокация
        const enabled = await Location.hasServicesEnabledAsync();

        if (!enabled) {
            Alert.alert(
                'Геолокация выключена',
                'Включите Location в Android Emulator'
            );

            return;
        }

        let currentLocation = await Location.getLastKnownPositionAsync();

        if (!currentLocation) {
            currentLocation = await Location.getCurrentPositionAsync({
                accuracy: Location.Accuracy.Balanced
            });
        }

        if (!currentLocation) {
            Alert.alert('Ошибка', 'Не удалось получить координаты');
            return;
        }

        setLocation({
            latitude: currentLocation.coords.latitude,
            longitude: currentLocation.coords.longitude
        });

        const addresses = await Location.reverseGeocodeAsync({
            latitude: currentLocation.coords.latitude,
            longitude: currentLocation.coords.longitude
        });

        if (addresses.length > 0) {
            const addr = addresses[0];

            const addressString = [
                addr.street,
                addr.city,
                addr.country
            ]
                .filter(Boolean)
                .join(', ');

            setAddress(addressString);
        }
    } catch (error) {
        console.log('LOCATION ERROR:', error);

        Alert.alert(
            'Ошибка геолокации',
            'Эмулятор Android не смог получить GPS'
        );
    } finally {
        setIsLoadingLoc(false);
    }
};

    const takePhoto = async () => {
        const { status } = await ImagePicker.requestCameraPermissionsAsync();
        if (status !== 'granted') return Alert.alert('Ошибка', 'Нужен доступ к камере');

        const result = await ImagePicker.launchCameraAsync({ quality: 0.8 });
        if (!result.canceled && result.assets) {
            setPhotoUri(result.assets[0].uri);
        }
    };

    const handleSave = async () => {
        if (!title.trim() || !content.trim() || !location) return;
        
        setIsSaving(true);
        try {
            const newNote: GeoNote = {
                id: uuidv4(),
                title: title.trim(),
                content: content.trim(),
                latitude: location.latitude,
                longitude: location.longitude,
                address, photoUri,
                createdAt: Date.now()
            };
            await dispatch(saveNote(newNote)).unwrap();
            navigation.goBack();
        } catch (error) {
            Alert.alert('Ошибка', 'Не удалось сохранить');
        } finally {
            setIsSaving(false);
        }
    };

    const isBtnDisabled = !title.trim() || !content.trim() || !location || isSaving;

    return (
        <ScrollView style={styles.container}>
            <View style={styles.form}>
                <Text style={styles.label}>Заголовок</Text>
                <TextInput style={styles.input} value={title} onChangeText={setTitle} placeholder="Введите заголовок" />

                <Text style={styles.label}>Содержание</Text>
                <TextInput style={[styles.input, { minHeight: 100 }]} value={content} onChangeText={setContent} multiline textAlignVertical="top" />

                <Text style={styles.label}>Местоположение</Text>
                {isLoadingLoc ? <ActivityIndicator size="small" /> : location ? (
                    <Text style={styles.locationText}>📍 {address || `${location.latitude.toFixed(4)}, ${location.longitude.toFixed(4)}`}</Text>
                ) : (
                    <TouchableOpacity style={styles.btnSecondary} onPress={getCurrentLocation}><Text>Получить гео</Text></TouchableOpacity>
                )}

                <Text style={[styles.label, { marginTop: 16 }]}>Фото</Text>
                <TouchableOpacity style={styles.btnSecondary} onPress={takePhoto}>
                    <Text>{photoUri ? '📸 Переснять' : '📷 Сделать фото'}</Text>
                </TouchableOpacity>

                {photoUri && (
                    <View style={styles.previewContainer}>
                        <Image source={{ uri: photoUri }} style={styles.preview} />
                        <TouchableOpacity style={styles.removeBtn} onPress={() => setPhotoUri(undefined)}>
                            <Text style={styles.removeText}>✕</Text>
                        </TouchableOpacity>
                    </View>
                )}

                <TouchableOpacity 
                    style={[styles.saveBtn, isBtnDisabled && { backgroundColor: '#ccc' }]} 
                    onPress={handleSave} 
                    disabled={isBtnDisabled}
                >
                    {isSaving ? <ActivityIndicator color="white" /> : <Text style={styles.saveBtnText}>Сохранить</Text>}
                </TouchableOpacity>
            </View>
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f5f5f5' },
    form: { padding: 16 },
    label: { fontSize: 16, fontWeight: 'bold', marginBottom: 8, color: '#333' },
    input: { backgroundColor: 'white', padding: 12, borderRadius: 8, marginBottom: 16, borderWidth: 1, borderColor: '#ddd' },
    locationText: { color: '#007AFF', marginBottom: 16 },
    btnSecondary: { backgroundColor: '#e1f5fe', padding: 12, borderRadius: 8, alignItems: 'center' },
    previewContainer: { marginTop: 12, position: 'relative' },
    preview: { width: '100%', height: 200, borderRadius: 8 },
    removeBtn: { position: 'absolute', top: 8, right: 8, backgroundColor: 'rgba(0,0,0,0.5)', width: 30, height: 30, borderRadius: 15, justifyContent: 'center', alignItems: 'center' },
    removeText: { color: 'white', fontWeight: 'bold' },
    saveBtn: { backgroundColor: '#007AFF', padding: 16, borderRadius: 8, alignItems: 'center', marginTop: 24 },
    saveBtnText: { color: 'white', fontWeight: 'bold', fontSize: 16 }
});