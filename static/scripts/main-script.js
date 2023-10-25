// Enforcing strict mode to catch common coding mistakes
'use strict';

// Get the button element for booking and store it in the variable 'bookingBtn'
const bookingBtn = document.getElementById('book-appointment');
const findTeacherBtn = document.getElementById('find-teacher');
// Asynchronous function to send the booking data to the server
async function sendBooking(newBooking) {
  try {
    // Creating a FormData object to hold the booking data
    const formData = new FormData();

    // Looping through the properties of newBooking and appending them to formData
    for (const key in newBooking) {
      formData.append(key, newBooking[key]);
    }

    // Sending a POST request to the server with the booking data
    const response = await fetch('/bookappointment', {
      method: 'POST',
      body: formData,
    });

    // Checking if the response status is not OK (200-299)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Parsing the JSON response from the server
    const data = await response.json();

    // Logging the server response to the console
    console.log('Success:', data);

    // Calling a function to display the booking confirmation, passing the parsed data
    displayBookingConfirmation(data);
  } catch (error) {
    // Logging any errors to the console
    console.error('Error:', error);
    // Displaying the error message in the booking-details div
    displayBookingError(error);
  }
}

//
function displayBookingError(error) {
  const bookingDetailsDiv = document.getElementById('booking-details');

  // Constructing an HTML string with the error message
  const errorHtml = `
      <h2>Booking Error</h2>
      <p>Sorry, there was an error with your booking:</p>
      <p class="error-message">${error.message}</p>
  `;

  // Inserting the HTML string into the bookingDetailsDiv, thereby updating the webpage
  bookingDetailsDiv.innerHTML = errorHtml;
}

// Function to display the booking confirmation in the webpage
function displayBookingConfirmation(booking) {
  // Getting the div element to display the booking details
  const bookingDetailsDiv = document.getElementById('booking-details');

  // Constructing an HTML string with the booking details
  const confirmationHtml = `
      <h2>Booking Confirmation</h2>
      <p>Thank you for booking an appointment. Here are the details:</p>
      <ul>
          <li><strong>Parent Name:</strong> ${booking.parent}</li>
          <li><strong>Student Name:</strong> ${booking.student}</li>
          <li><strong>Teacher:</strong> ${booking.teacher}</li>
          <li><strong>Date:</strong> ${booking.date}</li>
          <li><strong>Time:</strong> ${booking.time}</li>
      </ul>
  `;

  // Inserting the HTML string into the bookingDetailsDiv, thereby updating the webpage
  bookingDetailsDiv.innerHTML = confirmationHtml;
}

// Adding a click event listener to the booking button
bookingBtn.addEventListener('click', function () {
  // Getting the input values from the form and storing them in variables
  const parentName = document.getElementById('parent-name').value;
  const studentName = document.getElementById('student-name').value;
  const teacher = document.getElementById('teacher').value;
  const date = document.getElementById('date').value;
  const time = document.getElementById('time').value;

  // Creating a new booking object with the input values
  const newBooking = {
    parentName,
    studentName,
    teacher,
    date,
    time,
  };

  // Calling the sendBooking function, passing the new booking data
  sendBooking(newBooking);

  // Resetting the form to clear the input fields
  document.getElementById('booking-form').reset();
});

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('teacherForm');

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const teacherName = document.getElementById('teacher_name').value;
    const encodedName = encodeURIComponent(teacherName).replace(/\+/g, '%20');
    window.location.href = `/show_appointments/${encodedName}`;
  });
});
