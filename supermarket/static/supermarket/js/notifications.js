// ==================== SYSTÈME DE NOTIFICATIONS ====================

let notificationsData = [];
let lastNotificationId = null;
let notificationCheckInterval = null;

// Son de notification (utilise l'API Web Audio)
function playNotificationSound() {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800; // Fréquence en Hz
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
    } catch (e) {
        console.log('Impossible de jouer le son:', e);
    }
}

// Charger les notifications
function loadNotifications(notificationsUrl) {
    fetch(notificationsUrl)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                notificationsData = data.notifications;
                updateNotificationBadge(data.nombre_non_lues);
                displayNotifications(notificationsData);
                
                // Vérifier s'il y a de nouvelles notifications
                if (notificationsData.length > 0) {
                    const firstNotification = notificationsData[0];
                    if (!firstNotification.lu && firstNotification.id !== lastNotificationId) {
                        playNotificationSound();
                        lastNotificationId = firstNotification.id;
                    }
                }
            }
        })
        .catch(error => {
            console.error('Erreur lors du chargement des notifications:', error);
        });
}

// Afficher les notifications
function displayNotifications(notifications) {
    const notificationsList = document.getElementById('notificationsList');
    if (!notificationsList) return;
    
    if (notifications.length === 0) {
        notificationsList.innerHTML = '<div style="padding: 20px; text-align: center; color: #6c757d;">Aucune notification</div>';
        return;
    }
    
    let html = '';
    notifications.forEach(notif => {
        const iconClass = getNotificationIcon(notif.type);
        const colorClass = getNotificationColor(notif.type);
        const isUnread = !notif.lu;
        
        html += `
            <div class="notification-item" data-id="${notif.id}" style="padding: 15px; border-bottom: 1px solid #e1e8ed; cursor: pointer; transition: background 0.2s; ${isUnread ? 'background: #f0f8ff;' : ''}" onclick="handleNotificationClick(${notif.id}, ${notif.commande_id || 'null'}, ${notif.livraison_id || 'null'}, '${notif.type}')">
                <div style="display: flex; gap: 12px;">
                    <div style="width: 40px; height: 40px; border-radius: 50%; background: ${colorClass}; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; flex-shrink: 0;">
                        <i class="${iconClass}"></i>
                    </div>
                    <div style="flex: 1;">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 5px;">
                            <h4 style="margin: 0; color: #2c3e50; font-size: 0.95em; font-weight: 600;">${notif.titre}</h4>
                            ${isUnread ? '<span style="width: 8px; height: 8px; background: #06beb6; border-radius: 50%; display: inline-block; margin-top: 5px;"></span>' : ''}
                        </div>
                        <p style="margin: 0; color: #6c757d; font-size: 0.85em; line-height: 1.4;">${notif.message}</p>
                        <div style="margin-top: 8px; color: #95a5a6; font-size: 0.75em;">${notif.date_creation}</div>
                    </div>
                </div>
            </div>
        `;
    });
    
    notificationsList.innerHTML = html;
}

// Obtenir l'icône selon le type de notification
function getNotificationIcon(type) {
    const icons = {
        'commande_enregistree': 'fas fa-shopping-cart',
        'livraison_planifiee': 'fas fa-truck',
        'livraison_confirmee': 'fas fa-check-circle',
        'livraison_terminee': 'fas fa-check-double',
        'stock_insuffisant': 'fas fa-exclamation-triangle',
        'autre': 'fas fa-bell'
    };
    return icons[type] || 'fas fa-bell';
}

// Obtenir la couleur selon le type de notification
function getNotificationColor(type) {
    const colors = {
        'commande_enregistree': '#3498db',
        'livraison_planifiee': '#17a2b8',
        'livraison_confirmee': '#28a745',
        'livraison_terminee': '#20c997',
        'stock_insuffisant': '#ffc107',
        'autre': '#6c757d'
    };
    return colors[type] || '#6c757d';
}

// Mettre à jour le badge de notification
function updateNotificationBadge(count) {
    const badge = document.getElementById('notificationBadge');
    if (badge) {
        if (count > 0) {
            badge.textContent = count > 99 ? '99+' : count;
            badge.style.display = 'flex';
        } else {
            badge.style.display = 'none';
        }
    }
}

// Basculer l'affichage des notifications
function toggleNotifications() {
    const dropdown = document.getElementById('notificationsDropdown');
    if (!dropdown) return;
    
    if (dropdown.style.display === 'none') {
        dropdown.style.display = 'block';
        const notificationsUrl = document.getElementById('notificationsUrl')?.value || '{% url "get_notifications" %}';
        loadNotifications(notificationsUrl);
    } else {
        dropdown.style.display = 'none';
    }
}

// Gérer le clic sur une notification
function handleNotificationClick(notificationId, commandeId, livraisonId, type) {
    const markReadUrl = document.getElementById('markReadUrl')?.value || '{% url "marquer_notification_lue" 0 %}';
    const detailCommandeUrl = document.getElementById('detailCommandeUrl')?.value || '{% url "detail_commande" 0 %}';
    const voirItineraireUrl = document.getElementById('voirItineraireUrl')?.value || '{% url "voir_itineraire" %}';
    const consulterLivraisonsUrl = document.getElementById('consulterLivraisonsUrl')?.value || '{% url "consulter_livraisons" %}';
    
    // Marquer comme lue
    fetch(markReadUrl.replace('0', notificationId), {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateNotificationBadge(data.nombre_non_lues);
            const notificationsUrl = document.getElementById('notificationsUrl')?.value || '{% url "get_notifications" %}';
            loadNotifications(notificationsUrl);
        }
    });
    
    // Rediriger selon le type
    if (commandeId) {
        window.location.href = detailCommandeUrl.replace('0', commandeId);
    } else if (livraisonId) {
        if (type === 'livraison_planifiee' || type === 'livraison_confirmee') {
            window.location.href = voirItineraireUrl;
        } else {
            window.location.href = consulterLivraisonsUrl;
        }
    }
}

// Marquer toutes les notifications comme lues
function marquerToutesLues() {
    const markAllReadUrl = document.getElementById('markAllReadUrl')?.value || '{% url "marquer_toutes_notifications_lues" %}';
    
    fetch(markAllReadUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateNotificationBadge(0);
            const notificationsUrl = document.getElementById('notificationsUrl')?.value || '{% url "get_notifications" %}';
            loadNotifications(notificationsUrl);
        }
    });
}

// Obtenir le cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialiser le système de notifications
function initNotifications(notificationsUrl, checkInterval = 30000) {
    // Charger les notifications au chargement de la page
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            loadNotifications(notificationsUrl);
            
            // Vérifier les nouvelles notifications périodiquement
            notificationCheckInterval = setInterval(function() {
                loadNotifications(notificationsUrl);
            }, checkInterval);
        });
    } else {
        loadNotifications(notificationsUrl);
        
        // Vérifier les nouvelles notifications périodiquement
        notificationCheckInterval = setInterval(function() {
            loadNotifications(notificationsUrl);
        }, checkInterval);
    }
    
    // Fermer le dropdown en cliquant en dehors
    document.addEventListener('click', function(event) {
        const container = document.getElementById('notificationsContainer');
        const dropdown = document.getElementById('notificationsDropdown');
        if (container && dropdown && !container.contains(event.target)) {
            dropdown.style.display = 'none';
        }
    });
    
    // Nettoyer l'intervalle quand la page est fermée
    window.addEventListener('beforeunload', function() {
        if (notificationCheckInterval) {
            clearInterval(notificationCheckInterval);
        }
    });
}


