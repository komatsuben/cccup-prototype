// Function to update demo card based on form values.
function updateDemo() {
    const stage = document.getElementById('input-stage').value;
    const status = document.getElementById('input-status').value;
    const team1 = document.getElementById('input-team1').value;
    const team2 = document.getElementById('input-team2').value;
    const team1Score = document.getElementById('input-team1-score').value;
    const team2Score = document.getElementById('input-team2-score').value;
    const time = document.getElementById('input-time').value;

    document.getElementById('demo-stage').innerText = stage || 'Stage';
    document.getElementById('demo-status').innerText = status || 'Status';
    document.getElementById('demo-team1').innerText = team1 || 'Team 1';
    document.getElementById('demo-team2').innerText = team2 || 'Team 2';
    document.getElementById('demo-team1-score').innerText = team1Score || '0';
    document.getElementById('demo-team2-score').innerText = team2Score || '0';
    document.getElementById('demo-time').innerText = time || 'YYYY-MM-DD HH:MM';
}

// Attach event listeners to all inputs to update demo on change
const inputs = document.querySelectorAll('#match-form input.form-control');
inputs.forEach(input => {
    input.addEventListener('input', updateDemo);
});

// Also attach to select fields if you have any (for status, stage, etc.)
const selects = document.querySelectorAll('#match-form select.form-control');
selects.forEach(select => {
    select.addEventListener('change', updateDemo);
});

// Initial call to update demo on page load
updateDemo();


//Function to handle popup
function togglePopup() {
    const popup = document.getElementById('popup');
    const everything = document.getElementById('mother');

    if (popup.style.display === 'block') {
        popup.style.display = 'none';
        everything.style.filter = 'none';
    } else {
        popup.style.display = 'block';
        everything.style.filter = 'blur(3px) grayscale(0.5)';
    }
}

// Function to handle dynamic searching
function filterItems() {
    let input = document.getElementById('searchInput').value.toLowerCase();
    let items = document.getElementsByClassName('matches__container');

    for (let i = 0; i < items.length; i++) {
        let text = items[i].textContent.toLowerCase();
        if (text.includes(input)) {
            items[i].classList.remove('hidden');
        } else {
            items[i].classList.add('hidden');
        }
    }
}