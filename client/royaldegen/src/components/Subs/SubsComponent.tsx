import React, { useEffect, useState } from "react";
import "./SubsComponent.css";

type Subscription = {
  id: number;
  name: string;
  price: number;
  duration_days: number;
  description: string;
  max_words: number | null;
  access_to_best_model: boolean;
};

const SubsComponent: React.FC = () => {
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSubscriptions = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/subscriptions");

        if (!response.ok) {
          const errorData = await response.json();
          setError(errorData.detail || "Failed to fetch subscriptions.");
          return;
        }

        const data = await response.json();
        setSubscriptions(data);
      } catch (err) {
        console.error("Error fetching subscriptions:", err);
        setError("An error occurred while fetching subscriptions.");
      }
    };

    fetchSubscriptions();
  }, []);

  const handleSubscribe = (subscriptionId: number) => {
    alert(`Subscribed to plan with ID: ${subscriptionId}`);
  };

  return (
    <div className="subs-container">
      <h2>Subscription Plans</h2>
      {error && <p className="error">{error}</p>}
      {subscriptions.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Price</th>
              <th>Duration (Days)</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {subscriptions.map((sub) => (
              <tr key={sub.id}>
                <td>{sub.name}</td>
                <td>${sub.price.toFixed(2)}</td>
                <td>{sub.duration_days}</td>
                <td>{sub.description}</td>
                <td>
                  <button onClick={() => handleSubscribe(sub.id)}>
                    Subscribe
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No subscriptions available.</p>
      )}
    </div>
  );
};

export default SubsComponent;
