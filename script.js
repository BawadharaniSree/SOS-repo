
document.getElementById('loginForm').addEventListener('submit', function (e) {
   e.preventDefault(); // Prevent form submission
 
   const username = document.getElementById('username').value;
   const password = document.getElementById('password').value;
 
   if (username && password) {
     alert('Login Successful!\nUsername: ' + username);
     // You can replace this with actual API calls or further logic
   } else {
     alert('Please fill in all fields.');
   }
 });

 document.getElementById('signupForm').addEventListener('submit', function (e) {
   e.preventDefault(); // Prevent form submission
 
   const fullname = document.getElementById('fullname').value;
   const email = document.getElementById('email').value;
   const mobile = document.getElementById('mobile').value;
   const address = document.getElementById('address').value;
   const aadhar = document.getElementById('aadhar').value;
   const password = document.getElementById('password').value;
   const confirmPassword = document.getElementById('confirm-password').value;
 
   if (!fullname || !email || !mobile || !address || !aadhar || !password || !confirmPassword) {
     alert('Please fill in all fields.');
     return;
   }
 
   if (password !== confirmPassword) {
     alert('Passwords do not match.');
     return;
   }
 
   alert('Sign Up Successful!\nFull Name: ' + fullname + '\nEmail: ' + email);
   // You can replace this with actual API calls or further logic
 });