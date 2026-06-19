function ProductCard({ product }) {
    const BASEURL = import.meta.env.VITE_DJANGO_BASE_URL;
  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg p-4">
      <img
        src={`${BASEURL}${product.image}`}
        alt={product.name}
        className="w-full h-48 object-cover rounded-lg mb-4"
      />
      <h2 className="text-lg font-semibold text-gray-800 truncate">{product.name}</h2>
      <p className="text-gray-700 mb-2">{product.description}</p>
      <p className="text-gray-900 font-medium">${product.price}</p>
    </div>
  );
}

export default ProductCard;