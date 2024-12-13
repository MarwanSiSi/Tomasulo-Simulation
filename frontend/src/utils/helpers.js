// Helper function to create empty arithmetic station
export const createEmptyStation = () => ({
  busy: false,
  op: null,
  vj: null,
  vk: null,
  qj: null,
  qk: null,
  address: null,
});

// Helper function to create stations dynamically
export const createStations = (prefix, size) => {
  return Array(size)
    .fill()
    .reduce(
      (acc, _, idx) => ({
        ...acc,
        [`${prefix}${idx + 1}`]: createEmptyStation(),
      }),
      {}
    );
};
