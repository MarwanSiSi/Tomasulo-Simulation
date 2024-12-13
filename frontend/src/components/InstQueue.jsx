import PropTypes from "prop-types";

const InstructionQueue = ({ instructions }) => {
  return (
    <div className="border rounded-lg shadow-md max-w-md">
      <div className="bg-gray-100 p-3 border-b font-semibold text-lg">
        Instruction Queue
      </div>
      <div className="divide-y">
        {instructions.length > 0 ? (
          instructions.map((instruction, index) => (
            <div
              key={index}
              className={`p-3 ${
                index === 0 ? "bg-blue-50" : "bg-white"
              } hover:bg-gray-50 transition-colors duration-200`}
            >
              {instruction}
            </div>
          ))
        ) : (
          <div className="text-center text-gray-500 p-4">Queue is empty</div>
        )}
      </div>
    </div>
  );
};
InstructionQueue.propTypes = {
  instructions: PropTypes.array.isRequired,
};

export default InstructionQueue;
