function deleteArea(areaId) {
    if (confirm('Are you sure you want to delete this area?')) {
        fetch(`${removeAreaUrl}${areaId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                document.getElementById(`area-${areaId}`).remove();
            } else {
                alert('Failed to delete the area.');
            }
        });
    }
}