import PropTypes from "prop-types";

const Cache = ({ data = {} }) => {
  return (
    <>
      <h2 className="text-xl font-bold">Cache Contents</h2>
      <div className="w-full max-w-2xl border rounded-lg shadow-sm mt-5">
        <div className="overflow-y-auto max-h-40">
          <table className="w-full">
            <thead className="bg-gray-50 sticky top-0">
              <tr>
                <th className="px-4 py-2 border-b text-center">Address</th>
                <th className="px-4 py-2 border-b text-center">Value</th>
              </tr>
            </thead>
            <tbody>
              {Object.keys(data).length > 0 ? (
                Object.entries(data).map((entry, index) => {
                  return (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-4 py-2 border-b font-mono text-center">
                        {entry[0]}
                      </td>
                      <td className="px-4 py-2 border-b font-mono text-center">
                        {entry[1]}
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td
                    colSpan={2}
                    className="px-4 py-8 text-center text-gray-500"
                  >
                    Cache is empty
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
};
Cache.propTypes = {
  data: PropTypes.object,
};

export default Cache;
