import PropTypes from "prop-types";

const RegisterStatusTable = ({ registers }) => {
  return (
    <div>
      <h2 className="text-xl font-bold mb-2">Register Status</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full border">
          <thead className="bg-gray-100">
            <tr>
              <th className="border p-2">Register</th>
              <th className="border p-2">Value</th>
              <th className="border p-2">Busy</th>
              <th className="border p-2">Station</th>
            </tr>
          </thead>
          <tbody>
            {registers.map((reg, idx) => (
              <tr key={idx}>
                <td className="border p-2">F{idx}</td>
                <td className="border p-2">{reg.value}</td>
                <td className="border p-2">{reg.busy ? "Yes" : "No"}</td>
                <td className="border p-2">{reg.station || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RegisterStatusTable;

RegisterStatusTable.propTypes = {
  registers: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.number.isRequired,
      busy: PropTypes.bool.isRequired,
      station: PropTypes.string,
    })
  ).isRequired,
};
