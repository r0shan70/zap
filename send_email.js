const AWS = require('aws-sdk');

const SES = new AWS.SES({
  region: process.env.AWS_REGION
});

const params = {
  Destination: {
    ToAddresses: [process.env.RECIPIENT_EMAIL]
  },
  Message: {
    Body: {
      Text: {
        Data: 'Hello from AWS SES!'
      }
    },
    Subject: {
      Data: 'Test Email'
    }
  },
  Source: process.env.SENDER_EMAIL
};

SES.sendEmail(params, (err, data) => {
  if (err) {
    console.error('Error sending email:', err);
  } else {
    console.log('Email sent:', data);
  }
});
