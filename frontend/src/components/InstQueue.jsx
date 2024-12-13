import PropTypes from "prop-types";

const InstructionQueue = ({ instructions }) => {
  return (
    <div className="min-w-[400px]">
      <h2 className="text-xl font-bold mb-2">Instruction Queue</h2>
      <div className="overflow-y-auto max-h-56">
        <table className="min-w-full border ">
          <tbody>
            {/* {instructions?.length > 0 ? (
              instructions?.map((instruction, index) => (
                <tr key={index}>
                  <td className="border p-2 text-center">{instruction}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td className="border p-2 text-center text-gray-500">Empty</td>
              </tr>
            )} */}
            {instructions?.map((instruction, index) => (
              <tr key={index}>
                <td className="border p-2 text-center">{instruction}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
InstructionQueue.propTypes = {
  instructions: PropTypes.array,
};

export default InstructionQueue;
