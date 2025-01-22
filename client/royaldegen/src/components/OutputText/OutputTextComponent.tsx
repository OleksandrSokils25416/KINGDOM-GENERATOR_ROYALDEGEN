import { useEffect, useState } from "react";
import "./OutputTextComponent.css";

interface Props {
  text: string;
}

const OutputTextComponent = ({ text }: Props) => {
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (text) {

      const timer = setTimeout(() => {
        setLoading(false);
      }, 3000);

      return () => clearTimeout(timer);
    } else {
      setLoading(true);
    }
  }, [text]);

  return (
    <div className="output-text-container">
      {loading ? (
        <div className="skeleton-loader">
          <div className="skeleton-line"></div>
          <div className="skeleton-line"></div>
          <div className="skeleton-line short"></div>
        </div>
      ) : (
        <p>{text || "Your generated text will appear here."}</p>
      )}
    </div>
  );
};

export default OutputTextComponent;
