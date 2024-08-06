function deleteArea(areaId) {
    if (confirm('Are you sure you want to delete this area?')) {
        fetch(`{% url 'better_buildings:remove_area' 0 %}`.replace('0', areaId), {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
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