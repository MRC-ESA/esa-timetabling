let bookings = [];

document
  .getElementById('book-appointment')
  .addEventListener('click', function () {
    const parentName = document.getElementById('parent-name').value;
    const studentName = document.getElementById('student-name').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;

    const newBooking = {
      parentName,
      studentName,
      date,
      time,
    };

    bookings.push(newBooking);

    document.getElementById('booking-details').textContent = JSON.stringify(
      bookings,
      null,
      2
    );

    // Send POST request to Flask server
    async function sendBooking(newBooking) {
      try {
        const response = await fetch('/bookappointment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newBooking),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Success:', data);
      } catch (error) {
        console.error('Error:', error);
      }
    }

    // Reset the form
    document.getElementById('booking-form').reset();
  });
