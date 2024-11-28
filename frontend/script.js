// frontend/script.js

const personInput = document.getElementById('person-input');
const goButton = document.getElementById('go-button');
const resultDiv = document.getElementById('result');

goButton.addEventListener('click', async () => {
  const personName = personInput.value.trim();
  if (!personName) {
    alert('Please enter a person\'s name.');
    return;
  }

  // Show loading state
  resultDiv.innerHTML = '<p>Loading...</p>';

  try {
    const response = await fetch('http://localhost:5000/api/player-info', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name: personName }) // Send 'name' instead of 'player'
    });

    const data = await response.json();

    if (response.ok) {
      if (data.biography) {
        // Display biography
        const bioList = document.createElement('ul');
        bioList.className = 'biography';
        data.biography.forEach(point => {
          const listItem = document.createElement('li');
          listItem.textContent = point;
          bioList.appendChild(listItem);
        });

        // Display image if available
        if (data.imageUrl) {
          const img = document.createElement('img');
          img.src = data.imageUrl;
          img.alt = `${personName} Image`;
          img.className = 'person-image';
          resultDiv.innerHTML = '';
          resultDiv.appendChild(bioList);
          resultDiv.appendChild(img);
        } else if (data.message === "Sorry, don't know him/her.") {
          resultDiv.innerHTML = `<p>${data.message}</p>`;
        } else {
          resultDiv.innerHTML = '';
          resultDiv.appendChild(bioList);
          const noImage = document.createElement('p');
          noImage.textContent = 'Image not available.';
          resultDiv.appendChild(noImage);
        }
      } else if (data.message) {
        // Display message (e.g., person not found)
        resultDiv.innerHTML = `<p>${data.message}</p>`;
      } else {
        resultDiv.innerHTML = '<p>Unexpected response from the server.</p>';
      }
    } else {
      resultDiv.innerHTML = `<p>Error: ${data.message}</p>`;
    }
  } catch (error) {
    console.error(error);
    resultDiv.innerHTML = '<p>Something went wrong. Please try again later.</p>';
  }
});
