import "./OutputTextComponent.css";

interface Props {
  text: string;
}

const OutputTextComponent = ({ text }: Props) => {
  return (
    <div className="output-text-container">
      <p>{text || "Your generated text will appear here."}</p>
    </div>
  );
};

export default OutputTextComponent;
