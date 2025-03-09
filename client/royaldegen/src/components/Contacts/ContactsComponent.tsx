import React from "react";
import "./ContactsComponent.css";

const ContactsComponent: React.FC = () => {
  return (
    <div className="contacts-container">
      <h2>Contacts</h2>
      <p className="contact-text">If you want to discuss any custom subscription plan, please contact us:</p>
      <p className="contact-text">
        <strong>Phone:</strong> +48 585 80085 9
      </p>
      <p className="contact-text">
        <strong>Email:</strong> template@doom.halo
      </p>
      <p className="contact-text">
        <strong>Address:</strong> Somewhere in Nevada
      </p>
    </div>
  );
};

export default ContactsComponent;