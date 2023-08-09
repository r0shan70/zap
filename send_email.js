const AWS = require('aws-sdk');

 

AWS.config.update({
  accessKeyId: process.env.AKIAQ5OENXUUTLYD4Z5K,
  secretAccessKey: process.env.yQpxkeHicwUbKIY/ZFEyNUAKZVtfxU+7iV/xwqLh,
  region: 'eu-northt-1', // Change to your desired AWS region
});

 

const ses = new AWS.SES({ apiVersion: '2010-12-01' });

 

const params = {
  Destination: {
    ToAddresses: [process.env.TO_EMAIL],
  },
  Message: {
    Body: {
      Text: {
        Charset: 'UTF-8',
        Data: 'This is the email body.',
      },
    },
    Subject: {
      Charset: 'UTF-8',
      Data: 'Email Subject',
    },
  },
  Source: process.env.FROM_EMAIL,
};

 

ses.sendEmail(params, (err, data) => {
  if (err) {
    console.error('Error sending email:', err);
  } else {
    console.log('Email sent successfully:', data);
  }
});
