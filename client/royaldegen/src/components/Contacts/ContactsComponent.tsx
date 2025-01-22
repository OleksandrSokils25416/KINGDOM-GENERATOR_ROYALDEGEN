import React from "react";
import "./ContactsComponent.css";

const ContactsComponent: React.FC = () => {
  return (
    <div className="contacts-container">
      <h2>Contacts</h2>
      <p className="contact-text">If you want to discuss any custom subscription plan, please contact us:</p>
      <p className="contact-text">
        <strong>Phone:</strong> +8 800 555-35-35
      </p>
      <p className="contact-text">
        <strong>Email:</strong> ivan.zolo_2004@yandex.ru
      </p>
      <p className="contact-text">
        <strong>Address:</strong> Pushkin's street, Kolotushkin's house
      </p>
    </div>
  );
};

export default ContactsComponent;