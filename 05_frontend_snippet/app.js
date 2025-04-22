document.addEventListener('DOMContentLoaded', function () {
    const emailInput = document.getElementById('eligibility-email');
    const checkButton = document.getElementById('check-eligibility');
    const resultDiv = document.getElementById('result');
  
    checkButton.addEventListener('click', function () {
      const email = emailInput.value.trim();
  
      if (!email) {
        resultDiv.textContent = 'Please enter an email address.';
        resultDiv.style.color = 'red';
        return;
      }
        // TODO: Simulate an eligibility check
      console.log('Checking eligibility for:', email);
    });
  });
  